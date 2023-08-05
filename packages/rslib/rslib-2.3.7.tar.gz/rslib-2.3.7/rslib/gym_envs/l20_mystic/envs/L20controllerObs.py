from rslib.core.FeatureUtil import FeatureUtil
# from rslib.core.FeatureUtil_deb import FeatureUtil
import tensorflow as tf
import numpy as np
from functools import reduce


class controllerObs(object):
    '''

    '''

    def __init__(self, config, model, modelfile, sess, src, batch_size=None, one_step=False, use_rule=False, test=False):
        self.config = config
        self.FeatureUtil = FeatureUtil(config)
        self.model = model
        # saver = tf.train.Saver()
        # sess = tf.keras.backend.get_session()
        # saver.restore(sess, modelfile)

        self.item_emb1 = self.model.get_layer('embedding_1').get_weights()[0]
        self.item_emb2 = self.model.get_layer('embedding_2').get_weights()[0]
        self.item_embs = [self.item_emb1, self.item_emb2]

        # self.mid_layer_model = tf.keras.backend.function(self.model.input, self.model.get_layer('tf_op_layer_mean/mean').output)
        self.mid_layer_model = tf.keras.backend.function(self.model.input, self.model.get_layer('concatenate_1').output)
        # self.mid_layer_model = tf.keras.backend.function(self.model.input, self.model.get_layer('lstm').output)

        self.sess = sess
        self.src = src
        self.batch_size = batch_size
        self.one_step = one_step
        self.use_rule = use_rule
        self.test = test

        self.l1_mask = np.tile(self.src.l1_mask, [self.batch_size, 1])
        self.l2_mask = np.tile(self.src.l2_mask, [self.batch_size, 1])
        self.l3_mask = np.tile(self.src.l3_mask, [self.batch_size, 1])
        self.t0_mask = np.tile(self.src.t0_mask, [self.batch_size, 1])
        self.t1_mask = np.tile(self.src.t1_mask, [self.batch_size, 1])
        self.t2_mask = np.tile(self.src.t2_mask, [self.batch_size, 1])
        self.t3_mask = np.tile(self.src.t3_mask, [self.batch_size, 1])
        self.t4_mask = np.tile(self.src.t4_mask, [self.batch_size, 1])
        self.l0_ssr_mask = np.tile(self.src.l0_ssr_mask, [self.batch_size, 1])
        self.not_l0_ssr_mask = 1 - self.l0_ssr_mask
        self.taohua_mask = np.tile(self.src.taohua_mask, [self.batch_size, 1])
        self.not_taohua_mask = 1 - self.taohua_mask

        self.one_mask = np.ones_like(self.l1_mask)

    def get_item_emb(self, itemid):
        if int(itemid) >= 0:
            emb = np.array([x[int(itemid)] for x in self.item_embs])
            return np.max(emb, axis=0)
        else:
            return np.zeros(len(self.item_embs[0][0]))

    def keras_emb(self, rawstate):
        feat = self.FeatureUtil.feature_extraction(rawstate, serving=True)
        session = self.sess
        with session.as_default():
            with session.graph.as_default():
                mid_layer_output = self.mid_layer_model(feat)

        return mid_layer_output if self.batch_size else mid_layer_output[0]

    def action_mask(self, step, selected_embs):
        # if step < 3:
        #     if step == 0:
        #         l_mask = self.src.l1_mask
        #         t_mask = self.src.t3_mask | self.src.t4_mask
        #     elif step == 1:
        #         l_mask = self.src.l1_mask
        #         t_mask = self.src.t2_mask | self.src.t3_mask | self.src.t4_mask
        #     else:
        #         l_mask = self.src.l1_mask
        #         t_mask = self.src.t0_mask
        # elif step < 6:
        #     if step == 3:
        #         l_mask = self.src.l2_mask
        #         t_mask = self.src.t1_mask | self.src.t2_mask
        #     elif step == 4:
        #         l_mask = self.src.l2_mask
        #         t_mask = self.src.t3_mask | self.src.t4_mask
        #     else:
        #         l_mask = self.src.l2_mask
        #         t_mask = self.src.t0_mask
        # else:
        #     if step == 6:
        #         l_mask = self.src.l3_mask
        #         t_mask = self.src.t1_mask
        #     elif step == 7:
        #         l_mask = self.src.l3_mask
        #         t_mask = self.src.t3_mask | self.src.t4_mask
        #     else:
        #         l_mask = self.src.l3_mask
        #         t_mask = self.src.t0_mask
        if not self.test:
            if_ssr_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.5),
                                   self.one_mask,
                                   self.not_l0_ssr_mask)
            if_taohua_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.8),
                                      self.one_mask,
                                      self.not_taohua_mask)
            if_l2_taohua_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.2),
                                         self.one_mask,
                                         self.not_taohua_mask)
            taohua_ajust_mask = np.less(np.random.random((self.batch_size,)), 0.5)
        else:
            if_ssr_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.1),
                                   self.one_mask,
                                   self.not_l0_ssr_mask)
            if_taohua_mask = np.where(np.less(np.random.random((self.batch_size,)), 1.0),
                                      self.one_mask,
                                      self.not_taohua_mask)
            if_l2_taohua_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.2),
                                         self.one_mask,
                                         self.not_taohua_mask)
            taohua_ajust_mask = np.less(np.random.random((self.batch_size,)), 0.0)

        if step < 3:
            if step == 0:
                l_mask = self.l1_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.5),
                                  self.t2_mask,
                                  self.t4_mask)
            elif step == 1:
                l_mask = self.l1_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.65),
                                  self.t2_mask,
                                  self.t4_mask)
            else:
                l_mask = self.l1_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.65),
                                  self.t3_mask,
                                  self.t4_mask)
        elif step < 6:
            if step == 3:
                l_mask = self.l2_mask
                t_mask = self.t1_mask
            elif step == 4:
                l_mask = self.l2_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.65),
                                  self.t2_mask,
                                  self.t4_mask)
            else:
                l_mask = self.l2_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.65),
                                  self.t3_mask,
                                  self.t4_mask)
        else:
            if step == 6:
                l_mask = self.l3_mask
                t_mask = self.t1_mask
            elif step == 7:
                l_mask = self.l3_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.8),
                                  self.t2_mask,
                                  self.t4_mask)
            else:
                l_mask = self.l3_mask
                t_mask = np.where(np.less(np.random.random((self.batch_size,)), 0.65),
                                  self.t3_mask,
                                  self.t4_mask)

        if self.use_rule:
            lt_mask = l_mask & t_mask
        else:
            lt_mask = l_mask

        mask = lt_mask
        mask = mask * (1 - selected_embs)

        have_ssr = np.max(self.l0_ssr_mask * selected_embs, axis=1)
        ssr_mask = 1 - have_ssr * self.l0_ssr_mask
        # mask = mask * (-1 * (have_ssr_mask - 1))

        have_taohua = np.max(self.taohua_mask * selected_embs, axis=1)
        th_mask = 1 - have_taohua * self.taohua_mask
        # mask = mask * (-1 * (have_taohua_mask - 1))

        if step in [3, 4, 5]:
            th_mask = th_mask * if_l2_taohua_mask

        if step in [6]:
            th_mask = np.where(taohua_ajust_mask,
                               self.not_taohua_mask,
                               th_mask)

        mask = mask * th_mask * ssr_mask * if_ssr_mask * if_taohua_mask

        assert np.shape(mask)[-1] == 500
        return mask

    def step_onehot(self, step):
        step += 1
        onehot = np.array([[0] * (step - 1) + [1] + [0] * (10 - step)] * self.batch_size)
        return onehot

    def layer_onehot(self, layers):
        onehot = np.array([reduce(lambda x, y: x + ([0] * (y - 1) + [1] * (1 if 1 <= y <= 3 else 0) + [0] * (3 - y)), layers[:, batch_i], []) for batch_i in range(self.batch_size)])
        assert np.shape(onehot)[-1] == 27
        return onehot

    def paytype_onehot(self, paytypes):
        onehot = np.array([reduce(lambda x, y: x + ([0] * (y - 1) + [1] * (1 if 1 <= y <= 4 else 0) + [0] * (4 - y)), paytypes[:, batch_i], []) for batch_i in range(self.batch_size)])
        assert np.shape(onehot)[-1] == 36
        return onehot

    def select_onehot(self, actions):
        onehot = np.zeros([self.batch_size, 500], dtype=np.int32)
        index = np.arange(0, np.shape(actions)[0])[:, np.newaxis].repeat(np.shape(actions)[1], 1)
        onehot[index, actions] = 1
        return onehot

    def rawstate2obs(self, rawstate, info, step):
        if step == 0:
            self.hist_emb = self.keras_emb(rawstate)
        # a = self.item_emb1[info['actions']]
        if self.one_step:
            return self.hist_emb

        item_embs = np.concatenate([np.concatenate([item_emb[info['actions'][:step]],
                                                    np.zeros([9 - step, self.batch_size, np.shape(item_emb)[-1]], dtype=int)])
                                    for item_emb in self.item_embs], axis=2)
        item_emb = np.reshape(np.transpose(item_embs, [1, 0, 2]), [self.batch_size, -1])

        step_embs = self.step_onehot(step)
        layers_embs = self.layer_onehot(info['layers'])
        paytypes_embs = self.paytype_onehot(info['paytypes'])

        select_embs = self.select_onehot(np.transpose(info['actions'][:step], [1, 0]))

        action_mask = self.action_mask(step, select_embs)
        # action_mask = np.ones([self.batch_size,500])

        return np.concatenate([action_mask, select_embs, step_embs, self.hist_emb, item_emb, layers_embs, paytypes_embs], 1)

    def get_obs(self, new_rawstate, info, step):
        obs = self.rawstate2obs(new_rawstate, info, step)
        # print(np.shape(obs))
        return obs
