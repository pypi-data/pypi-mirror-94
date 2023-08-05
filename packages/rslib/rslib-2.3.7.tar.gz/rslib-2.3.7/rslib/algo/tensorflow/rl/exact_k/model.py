# -*- coding: utf-8 -*-
# /usr/bin/python2

from __future__ import print_function
import tensorflow as tf

from .layers import *
from .hyperparams import Hyperparams as hp
from .data_load_ml import *
from .modules import *
from .utils import *


class Generator:
    def __init__(self, l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, l0_ssr_mask, taohua_mask, new_item_1=None, new_item_2=None, new_item_3=None, is_training=True, user=None, item_cand=None, lr=0.001, temperature=1, item_id_map=None, train_sample='random', predict_sample='random'):
        # 输入特征

        # self.user = tf.placeholder(tf.float32, shape=(None, 1207), name='user')  # 779
        self.user = tf.placeholder(tf.float32, shape=(None, 256), name='user')  # 779
        # self.user = tf.placeholder(tf.float32, shape=(None, None), name='user')  # 779

        self.batch_size = tf.shape(self.user)[0]
        self.item_cand = tf.placeholder(tf.int32, shape=(None, hp.seq_length), name='item_cand')

        # 传入一个 mask, 代表哪些动作可选与不可选
        self.l1_mask = tf.cast(tf.constant(l1_mask, dtype=tf.int32), tf.bool)
        self.l2_mask = tf.cast(tf.constant(l2_mask, dtype=tf.int32), tf.bool)
        self.l3_mask = tf.cast(tf.constant(l3_mask, dtype=tf.int32), tf.bool)
        self.t0_mask = tf.cast(tf.constant(t0_mask, dtype=tf.int32), tf.bool)
        self.t1_mask = tf.cast(tf.constant(t1_mask, dtype=tf.int32), tf.bool)
        self.t2_mask = tf.cast(tf.constant(t2_mask, dtype=tf.int32), tf.bool)
        self.t3_mask = tf.cast(tf.constant(t3_mask, dtype=tf.int32), tf.bool)
        self.t4_mask = tf.cast(tf.constant(t4_mask, dtype=tf.int32), tf.bool)
        self.l0_ssr_mask = tf.cast(tf.constant(l0_ssr_mask, dtype=tf.int32), tf.bool)
        self.taohua_mask = tf.cast(tf.constant(taohua_mask, dtype=tf.int32), tf.bool)

        # define decoder inputs
        # self.decode_target_ids = tf.placeholder(dtype=tf.int32, shape=[self.batch_size, hp.res_length], name="decoder_target_ids")  # [batch_size, res_length]
        self.decode_target_ids = tf.placeholder(dtype=tf.int32, shape=[None, hp.res_length], name="decoder_target_ids")  # [batch_size, res_length]
        self.reward = tf.placeholder(dtype=tf.float32, shape=[None], name="reward")  # [batch_size]

        # Encoder
        with tf.variable_scope("encoder"):
            # region emb
            self.enc_user = tf.layers.dense(self.user, hp.hidden_units, activation=tf.nn.relu)  # (N, T_q, C)
            # enc_item = [batch_size, seq_len, hidden_units]
            self.enc_item = embedding(self.item_cand,
                                      vocab_size=500,
                                      num_units=hp.hidden_units,
                                      zero_pad=False,
                                      scale=True,
                                      scope='enc_item_embed',
                                      # reuse=not is_training,
                                      reuse=False
                                      )
            self.enc = tf.concat([tf.stack(hp.seq_length * [self.enc_user], axis=1), self.enc_item], axis=2)
            # endregion
            # region Dropout
            self.enc = tf.layers.dropout(self.enc,
                                         rate=hp.dropout_rate,
                                         training=tf.convert_to_tensor(is_training))
            # endregion
            # region squence
            if hp.use_mha:
                ## Blocks
                for i in range(hp.num_blocks):
                    with tf.variable_scope("num_blocks_{}".format(i)):
                        ### Multihead Attention
                        self.enc = multihead_attention(queries=self.enc,
                                                       keys=self.enc,
                                                       num_units=hp.hidden_units * 2,
                                                       num_heads=hp.num_heads,
                                                       dropout_rate=hp.dropout_rate,
                                                       is_training=is_training,
                                                       causality=False)

                        ### Feed Forward
                        self.enc = feedforward(self.enc, num_units=[4 * hp.hidden_units, hp.hidden_units * 2])
            else:
                cell = tf.nn.rnn_cell.GRUCell(num_units=hp.hidden_units * 2)
                outputs, _ = tf.nn.dynamic_rnn(cell=cell, inputs=self.enc, dtype=tf.float32)
                self.enc = outputs
            # endregion

        # Decoder
        with tf.variable_scope("decoder"):
            dec_cell = LSTMCell(hp.hidden_units * 2)

            if hp.num_layers > 1:
                cells = [dec_cell] * hp.num_layers
                dec_cell = MultiRNNCell(cells)
            # ptr sampling
            enc_init_state = trainable_initial_state(self.batch_size, dec_cell.state_size)

            custom_logits, custom_path, _ = ptn_rnn_decoder(
                dec_cell, None,
                self.enc, enc_init_state,
                hp.seq_length, hp.res_length, hp.hidden_units * 2,
                hp.num_glimpse, self.batch_size,
                self.l1_mask, self.l2_mask, self.l3_mask,
                self.t0_mask, self.t1_mask, self.t2_mask, self.t3_mask, self.t4_mask,
                l0_ssr_mask, taohua_mask,
                mode="CUSTOM", reuse=False, beam_size=None,
                temperature=temperature,
                train_sample=train_sample, predict_sample=predict_sample
            )
            # logits: [batch_size, res_length, seq_length]
            self.custom_logits = tf.identity(custom_logits, name="custom_logits")
            # sample_path: [batch_size, res_length]
            self.custom_path = tf.identity(custom_path, name="custom_path")
            self.custom_result = batch_gather(self.item_cand, self.custom_path)
            # id 转换
            if item_id_map is not None:
                id_map_table = tf.get_variable('id_map_table',
                                               shape=np.shape(item_id_map),
                                               initializer=tf.constant_initializer(item_id_map),
                                               trainable=False,
                                               dtype=tf.int64)
                self.custom_result_map = tf.identity(tf.nn.embedding_lookup(id_map_table, self.custom_result)[:, :, 0], 'custom_result_map')
                batch_size = tf.shape(self.custom_result_map)[0]

                # region 替换 ssr
                def replace_new_item(custom_result_map, layer, new_item):
                    if not new_item:
                        return custom_result_map
                    new_item_tf = tf.constant(new_item, dtype=tf.int64)
                    random_a = tf.random_uniform([1], 0, len(new_item), dtype=tf.int64)
                    random_a = tf.gather(new_item_tf, random_a)
                    # random_ssr = tf.py_func(np.random.choice, [self.new_item, 1], tf.int64)
                    random_a = tf.tile(random_a[tf.newaxis, :], [batch_size, 9])

                    random_b = tf.random_uniform([1], 0, 3, dtype=tf.int64)

                    mask0 = tf.cast(tf.one_hot(random_b, depth=3, on_value=1, off_value=0, dtype=tf.int32)[0], dtype=tf.int64)
                    mask1 = tf.convert_to_tensor([0, 0, 0], dtype=tf.int64)
                    mask2 = tf.convert_to_tensor([0, 0, 0], dtype=tf.int64)
                    if layer == 1:
                        mask = tf.concat([mask0, mask1, mask2], axis=0)
                    elif layer == 2:
                        mask = tf.concat([mask1, mask0, mask2], axis=0)
                    elif layer == 3:
                        mask = tf.concat([mask1, mask2, mask0], axis=0)
                    else:
                        mask = tf.convert_to_tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=tf.int64)

                    p = min(0.05 * len(new_item), 0.1)
                    new_fragment = tf.cast(tf.less(tf.random_uniform([1], 0, 1, dtype=tf.float32), p), tf.int64)
                    mask = new_fragment * mask
                    mask = tf.tile(mask[tf.newaxis, :], [batch_size, 1])
                    mask = tf.cast(mask, dtype=tf.bool)

                    custom_result_map = tf.where(mask, random_a, custom_result_map)
                    return custom_result_map
                # endregion
                self.custom_result_map = replace_new_item(self.custom_result_map, 1, new_item_1)
                self.custom_result_map = replace_new_item(self.custom_result_map, 2, new_item_2)
                self.custom_result_map = replace_new_item(self.custom_result_map, 3, new_item_3)

                # 打乱顺序
                custom_result_map_trans = tf.transpose(self.custom_result_map, [1, 0])
                self.custom_result_map_random = tf.transpose(tf.concat(
                    [tf.random_shuffle(custom_result_map_trans[0:3]),
                     tf.random_shuffle(custom_result_map_trans[3:6]),
                     tf.random_shuffle(custom_result_map_trans[6:9])],
                    axis=0
                ), [1, 0],
                    name='custom_result_map_random'
                )

            sampled_logits, sampled_path, _ = ptn_rnn_decoder(
                dec_cell, None,
                self.enc, enc_init_state,
                hp.seq_length, hp.res_length, hp.hidden_units * 2,
                hp.num_glimpse, self.batch_size,
                self.l1_mask, self.l2_mask, self.l3_mask,
                self.t0_mask, self.t1_mask, self.t2_mask, self.t3_mask, self.t4_mask,
                l0_ssr_mask, taohua_mask,
                mode="SAMPLE", reuse=True, beam_size=None,
                temperature=temperature,
                train_sample=train_sample, predict_sample=predict_sample
            )
            # logits: [batch_size, res_length, seq_length]
            self.sampled_logits = tf.identity(sampled_logits, name="sampled_logits")
            # sample_path: [batch_size, res_length]
            self.sampled_path = tf.identity(sampled_path, name="sampled_path")
            self.sampled_result = batch_gather(self.item_cand, self.sampled_path)
            if item_id_map is not None:
                self.sampled_result_map = tf.nn.embedding_lookup(id_map_table, self.sampled_result)[:, :, 0]

            # self.decode_target_ids is placeholder
            decoder_logits, _ = ptn_rnn_decoder(
                dec_cell, self.decode_target_ids,
                self.enc, enc_init_state,
                hp.seq_length, hp.res_length, hp.hidden_units * 2,
                hp.num_glimpse, self.batch_size,
                self.l1_mask, self.l2_mask, self.l3_mask,
                self.t0_mask, self.t1_mask, self.t2_mask, self.t3_mask, self.t4_mask,
                l0_ssr_mask, taohua_mask,
                mode="TRAIN", reuse=True, beam_size=None,
                temperature=1.0,
                train_sample=train_sample, predict_sample=predict_sample
            )
            self.dec_logits = tf.identity(decoder_logits, name="dec_logits")

            _, beam_path, _ = ptn_rnn_decoder(
                dec_cell, None,
                self.enc, enc_init_state,
                hp.seq_length, hp.res_length, hp.hidden_units * 2,
                hp.num_glimpse, self.batch_size,
                self.l1_mask, self.l2_mask, self.l3_mask,
                self.t0_mask, self.t1_mask, self.t2_mask, self.t3_mask, self.t4_mask,
                l0_ssr_mask, taohua_mask,
                mode="BEAMSEARCH", reuse=True, beam_size=hp.beam_size,
                temperature=temperature,
                train_sample=train_sample, predict_sample=predict_sample
            )
            self.beam_path = tf.identity(beam_path, name="beam_path")
            self.beam_result = batch_gather(self.item_cand, self.beam_path)

            _, greedy_path, _ = ptn_rnn_decoder(
                dec_cell, None,
                self.enc, enc_init_state,
                hp.seq_length, hp.res_length, hp.hidden_units * 2,
                hp.num_glimpse, self.batch_size,
                self.l1_mask, self.l2_mask, self.l3_mask,
                self.t0_mask, self.t1_mask, self.t2_mask, self.t3_mask, self.t4_mask,
                l0_ssr_mask, taohua_mask,
                mode="GREEDY", reuse=True, beam_size=None,
                temperature=temperature,
                train_sample=train_sample, predict_sample=predict_sample
            )
            self.greedy_path = tf.identity(greedy_path, name="greedy_path")
            self.greedy_result = batch_gather(self.item_cand, self.greedy_path)

        if is_training:
            # Loss
            # self.y_smoothed = label_smoothing(tf.one_hot(self.decode_target_ids, depth=hp.data_length))
            self.r_loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.dec_logits,
                                                                         labels=self.decode_target_ids)
            # reinforcement
            self.policy_loss = tf.reduce_mean(tf.reduce_sum(self.r_loss, axis=1) * self.reward)
            # supervised loss
            self.loss = self.policy_loss

            # Training Scheme
            self.global_step = tf.Variable(0, name='global_step', trainable=False)
            self.optimizer = tf.train.AdamOptimizer(learning_rate=lr, beta1=0.9, beta2=0.98, epsilon=1e-8)
            self.train_op = self.optimizer.minimize(self.loss, global_step=self.global_step)

        self.variables = tf.global_variables()


class Discriminator:
    def __init__(self, lr=0.005):
        # atrank_mean 112
        # atrank2 640
        self.user = tf.placeholder(tf.float32, shape=(None, 256), name='user')
        self.batch_size = tf.shape(self.user)[0]
        self.item_cand = tf.placeholder(tf.int32, shape=(None, hp.seq_length), name='item_cand')

        self.reward_target = tf.placeholder(dtype=tf.float32, shape=[None], name="reward")  # [batch_size]

        ## Embedding
        # self.enc_user = tf.layers.dense(self.user, hp.hidden_units, activation=tf.nn.relu)  # (N, T_q, C)

        # self.enc_item = embedding(self.item_cand,
        #                           vocab_size=500,
        #                           num_units=hp.hidden_units,
        #                           zero_pad=False,
        #                           scale=True,
        #                           scope='enc_item_embed',
        #                           reuse=not is_training)
        # self.enc = tf.concat([tf.stack(hp.seq_length * [self.enc_user], axis=1), self.enc_item], axis=2)

        dense0 = self.user
        dense1 = tf.layers.dense(dense0, 128, activation=tf.nn.relu)
        dense2 = tf.layers.dense(dense1, 128, activation=tf.nn.relu)
        dense3 = tf.layers.dense(dense2, 128, activation=tf.nn.relu)

        self.reward = tf.layers.dense(dense3, 1)[:, 0]

        self.td_error = tf.abs(self.reward_target - self.reward)
        self.loss = tf.square(self.td_error)

        # Training Scheme
        self.global_step = tf.Variable(0, name='global_step', trainable=False)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=lr, beta1=0.9, beta2=0.98, epsilon=1e-8)
        self.train_op = self.optimizer.minimize(self.loss, global_step=self.global_step)
