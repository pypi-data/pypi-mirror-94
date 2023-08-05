#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
Transformer

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""
import tensorflow as tf
import tensorflow.python.keras.backend as K

class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, config):
        self.supports_masking = False
        self.config = config
        super(AttentionLayer, self).__init__()

    def call(self, x, mask=None):
        # Embedding
        embeddings_2 = x[0]
        time = x[1]
        time_gap = x[2]
        print(embeddings_2.get_shape().as_list())
        print(time.get_shape().as_list())
        query_seq_encoding = tf.keras.layers.Attention()([embeddings_2, embeddings_2],mask=[time>0,time>0])
        query_encoding = tf.keras.layers.GlobalAveragePooling1D()(query_seq_encoding)
        return query_encoding

    # def compute_output_shape(self, input_shape):
    #     return (input_shape[0][0],input_shape[0][1])

    def compute_mask(self, input, input_mask=None):
        # need not to pass the mask to next layers
        return None

    def compute_output_shape(self, input_shape):
        return None, input_shape[-1]

class AttentionLayer2(tf.keras.layers.Layer):
    def __init__(self, config):
        self.supports_masking = False
        self.config = config
        super(AttentionLayer2, self).__init__()

    def call(self, x, mask=None):
        # Embedding
        embeddings = x
        # print(embeddings.get_shape().as_list())
        # time = x[1]
        # time_gap = x[2]
        # print(x.get_shape().as_list())
        # layers_emb_user_id = tf.keras.layers.Embedding(input_dim=5000000, output_dim=64)(embeddings)
        # print(layers_emb_user_id.get_shape().as_list())
        query_seq_encoding = tf.keras.layers.Attention()([embeddings, embeddings])
        query_encoding = tf.keras.layers.GlobalAveragePooling1D()(query_seq_encoding)
        return query_encoding

    # def compute_output_shape(self, input_shape):
    #     return (input_shape[0][0],input_shape[0][1])

    def compute_mask(self, input, input_mask=None):
        # need not to pass the mask to next layers
        return None

    def compute_output_shape(self, input_shape):
        return None, input_shape[-1]
