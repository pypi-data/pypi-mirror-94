import os
import json

import numpy as np
import tensorflow as tf
from tensorflow.python import keras
from tensorflow.python.keras import layers, regularizers
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from rslib.algo.tensorflow.layers.interaction import BiInteractionPooling
from rslib.algo.tensorflow.atrank.ATRankLayer import ATRankLayer, PositionalEncoding
from rslib.algo.tensorflow.utils import input_holder
from rslib.algo.tensorflow.utils.Input_processing import id_input_processing, cross_input_processing, sequence_embedding, sequence_group_embedding, sequence_tar_embedding
from rslib.algo.tensorflow.utils.model_compile import compile_model


def getInput(config, one_seq=False):
    '''定义了 RSLib 中所有模型的输入格式。

    在此处对 线上模型 与 离线模型 的输入分别做了处理，抽象为统一的输入格式

    Args:
        config: config
        one_seq: one_seq

    Returns:

    '''
    maxlen = config['maxlen']
    cross_feature_num = config['cross_feature_num']
    user_feature_num = config['user_feature_num']
    output_unit = config['output_unit']
    seq_num = config['seq_num']
    is_serving = config['is_serving']

    if is_serving:
        item_id_input = layers.Input(shape=(None,), dtype='int64', name='item_id_input')
    else:
        item_id_input = layers.Input(shape=(), dtype='int64', name='item_id_input')

    if one_seq:
        sequence_id_input = layers.Input(shape=(1, maxlen,), dtype='int64', name='sequence_id_input')
        sequence_time_input = layers.Input(shape=(1, maxlen,), dtype='int64', name='sequence_time_input')
        sequence_time_gaps_input = layers.Input(shape=(1, maxlen,), dtype='int64', name='sequence_time_gaps_input')
    else:
        sequence_id_input = layers.Input(shape=(seq_num, maxlen,), dtype='int64', name='sequence_id_input')
        sequence_time_input = layers.Input(shape=(seq_num, maxlen,), dtype='int64', name='sequence_time_input')
        sequence_time_gaps_input = layers.Input(shape=(seq_num, maxlen,), dtype='int64', name='sequence_time_gaps_input')
    if is_serving:
        cross_feature_indices_input = layers.Input(shape=(None, 2,), dtype='int64', name='cross_feature_indices_input')
        cross_feature_values_input = layers.Input(shape=(None,), dtype='float32', name='cross_feature_values_input')
        cross_feature_indices = layers.Lambda(lambda x: tf.reshape(x, (-1, 2)))(cross_feature_indices_input)
        cross_feature_values = layers.Lambda(lambda x: tf.reshape(x, [-1]))(cross_feature_values_input)
        cross_feature_input = layers.Lambda(lambda x: tf.SparseTensor(indices=x[0], values=x[1], dense_shape=[tf.shape(sequence_id_input)[0], cross_feature_num])) \
            ([cross_feature_indices, cross_feature_values])
    else:
        cross_feature_input = layers.Input(shape=(cross_feature_num,), dtype='float32', sparse=True, name='cross_feature_input')

    user_feature_input = layers.Input(shape=(user_feature_num,), dtype='int64', name='user_feature_input')
    # user_feature_input = Input(tensor=tf.zeros([tf.shape(sequence_id_input)[0], 12], dtype='int32'), name='user_feature_input')

    output_mask_input = layers.Input(shape=(output_unit,), dtype='float32', name='output_mask_input')
    # output_mask_input = layers.Input(shape=(300,), dtype='float32', name='output_mask_input')
    # output_mask_input = layers.Input(tensor=tf.ones([tf.shape(sequence_id_input)[0], 300], dtype='float32'), name='output_mask_input')
    # output_mask_input = Input(tensor=tf.ones([tf.shape(sequence_id_input)[0], 300], dtype='float32'), name='output_mask_input')
    cur_time_input = layers.Input(shape=(), dtype='int64', name='cur_time_input')

    if is_serving:
        return [item_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input], \
               [item_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_indices_input, cross_feature_values_input, user_feature_input, cur_time_input]
    else:
        return [item_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input], \
               [item_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, cur_time_input, output_mask_input]


class ATRank(object):

    def __init__(self, features, config, return_session=False):
        """Get a ATRank model.
        https://arxiv.org/abs/1711.06632

        Defines the input format of all models in RSLib. Here, the input of the online model and the offline model are processed separately and abstracted into a unified input format.

        Process sequence features, ID features, sparse features, etc.

        Ability to complete different forecasting tasks based on configuration files

        For different prediction tasks, set corresponding loss functions,
        At the same time, a variety of custom loss functions are built in.

        Args:
            config (dict): config, in which define many hyperparameter of the model, such as activation, hidden_unit and output_unit.See the tutorial for more details.
            return_session (bool): if True, return session of Tensorflow

        Returns:
            a ATRank model.
        """

        self.config = config
        item_unit = [1000] * len(features)

        class_num = config['class_num']
        emb_size = config['emb_size']

        activation = 'relu'
        hidden_unit = config['hidden_units']
        output_unit = config['output_unit']
        is_amp = config['is_amp']
        is_serving = config['is_serving']
        output_type = config['output_type']

        # todo，支持定制的输入格式

        # 商品id 映射 特征id
        item_maps = [layers.Embedding(input_dim=np.shape(w)[0], output_dim=1, weights=[w], trainable=False) for w in features]

        # 定义 特征embeddings
        item_embeddings = [layers.Embedding(input_dim=unit, output_dim=emb_size, embeddings_regularizer=regularizers.l2(0.01), embeddings_initializer="he_uniform") for unit in item_unit]

        [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input,
         user_feature_input, cur_time_input, output_mask_input], model_input = getInput(config)

        user_feature = id_input_processing(user_feature_input, config)
        cross_feature = cross_input_processing(cross_feature_input, config)

        # 对序列数据进行特殊处理
        batch_size = layers.Lambda(lambda x: tf.shape(role_id_input)[0])(1)
        if is_serving:
            item_id_input = role_id_input
            item_id_input = layers.Lambda(lambda x: tf.gather_nd(x, tf.where(x > 0)))(item_id_input)
        else:
            item_id_input = role_id_input

        # 获取待推荐物品序列
        item_id_input = layers.Lambda(
            lambda x: tf.reshape(x, [tf.shape(sequence_id_input)[0], tf.shape(x)[0] // tf.shape(sequence_id_input)[0]]))(item_id_input)
        # item_id_input = layers.Lambda(
        #     lambda x: tf.reshape(x, [batch_size, tf.shape(x)[0] // batch_size]), name='xxxx')(item_id_input)

        # 根据 商品id 获取 特征id
        item_feature_embs = []
        for item_map, item_embedding in zip(item_maps, item_embeddings):
            item_feature_id = item_map(item_id_input)
            item_feature_id = layers.Lambda(lambda x: x[:, :, 0])(item_feature_id)
            item_feature_emb = item_embedding(item_feature_id)
            item_feature_embs.append(item_feature_emb)
        item_feature = layers.concatenate(item_feature_embs)
        item_feature = layers.Dense(hidden_unit, activation='sigmoid', name='item_embedding')(item_feature)

        dense_all, time_mask_all = sequence_group_embedding(sequence_id_input, sequence_time_input, config)
        # dense_group_target, time_mask_group_target = sequence_tar_embedding(sequence_id_input, sequence_time_input, config)
        dense_group_target = item_feature
        # time_mask_group_target = layers.Lambda(lambda x: tf.constant(1, dtype=tf.int64, shape=[1, 1]))(1)
        time_mask_group_target = layers.Lambda(lambda x: tf.tile(tf.constant(1, dtype=tf.int64, shape=(1, 1)), tf.shape(dense_group_target)[:2]))(1)
        # dense_group_target2, _ = sequence_tar_embedding(sequence_id_input, sequence_time_input, config, target_seq=[2])

        seq_attention1 = ATRankLayer(config=config, type='encode', name='encode')([dense_all, dense_all], mask=[time_mask_all, time_mask_all], learning_phase=K.learning_phase())
        # seq_attention1 = ATRankLayer(config=config, type='encode', name='encode')(dense_all_with_pos, dense_all_with_pos, mask=[time_mask_all, time_mask_all], learning_phase=K.learning_phase())
        # seq_embedding1 = layers.Lambda(lambda x: tf.reduce_mean(x, axis=1), name='attention1_reduce')(seq_attention1)
        # seq_embedding1 = layers.Flatten()(seq_attention1)

        seq_attention2 = ATRankLayer(config=config, type='decode', name='decode')([seq_attention1, dense_group_target], mask=[time_mask_all, time_mask_group_target], learning_phase=K.learning_phase())
        # seq_attention2 = ATRankLayer(config=config, type='decode', name='decode')(seq_attention1, dense_group_target_with_pos, mask=[time_mask_all, time_mask_group_target], learning_phase=K.learning_phase())
        # seq_embedding2 = layers.Lambda(lambda x: tf.reduce_mean(x, axis=1), name='attention2_reduce')(seq_attention2)
        # seq_embedding2 = layers.Flatten()(seq_attention2)

        user_feature = layers.Concatenate(axis=-1)([user_feature, cross_feature])

        user_feature = layers.Lambda(lambda x: tf.tile(user_feature[:, tf.newaxis, :], [1, tf.shape(seq_attention2)[1], 1]))(1)

        # all_feature = layers.Concatenate(axis=-1)([ dense_group_target,dense_group_target])
        all_feature = layers.Concatenate(axis=-1)([seq_attention2, dense_group_target, user_feature])

        all_feature = layers.Dense(hidden_unit * 4, activation='sigmoid')(all_feature)
        output = layers.Dense(output_unit)(all_feature)
        output = layers.Lambda(lambda x: x[:, :, 0])(output)
        if not is_serving:
            if output_type in ['multi_class', 'multi_label']:
                paddings = tf.ones_like(output) * (-2 ** 32 + 1)
                output = tf.where(tf.equal(output_mask_input, 0), paddings, output)
            elif output_type in ['regression', 'multi_regression']:
                paddings = tf.zeros_like(output)
                output = tf.where(tf.equal(output_mask_input, 0), paddings, output)

        output_layer = {
            'multi_class': tf.nn.softmax,
            'multi_label': tf.sigmoid,
            'regression': lambda x: x,
            'multi_regression': lambda x: x
        }[output_type]
        output = output_layer(output)
        model = Model(inputs=model_input, outputs=[output])
        model, sess = compile_model(model, config)

        print(model.summary())

        self.model = model
        self.sess = sess
        # if return_session:
        #     return model, sess
        # else:
        #     return model

    def fit(self, **kwargs):
        self.model.fit(**kwargs)

    def get_item_embedding(self):
        config = self.config
        self.mid_layer_model = tf.keras.backend.function([self.model.input[0], self.model.input[1]], self.model.get_layer('item_embedding').output)

        a0 = np.array(range(1,1000))
        a1 = np.array([[1] for _ in range(config['seq_num'])])[np.newaxis, :]

        mid_layer_output = self.mid_layer_model([a0,a1])
        return mid_layer_output[0]
