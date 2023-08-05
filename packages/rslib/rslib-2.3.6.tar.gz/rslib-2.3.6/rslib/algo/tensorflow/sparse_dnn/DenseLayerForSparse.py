#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
DenseLayerForSparse

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

import tensorflow as tf
from tensorflow.python.keras.layers import *


class DenseLayerForSparse(tf.keras.layers.Layer):
    def __init__(self, vocabulary_size, num_units, activation, **kwargs):
        super(DenseLayerForSparse, self).__init__()
        self.vocabulary_size = vocabulary_size
        self.num_units = num_units
        self.activation = tf.keras.activations.get(activation)

    def build(self, input_shape):
        self.kernel = self.add_variable(
            "kernel", shape=[self.vocabulary_size, self.num_units]
        )
        self.bias = self.add_variable("bias", shape=[self.num_units])

    def call(self, inputs, **kwargs):
        if isinstance(inputs, tf.SparseTensor):
            outputs = tf.add(tf.sparse.matmul(inputs, self.kernel), self.bias)
        if not isinstance(inputs, tf.SparseTensor):
            outputs = tf.add(tf.matmul(inputs, self.kernel), self.bias)
        return self.activation(outputs)

    # def compute_output_shape(self, input_shape):
    #     input_shape = input_shape.get_shape().as_list()
    #     return input_shape[0], self.num_units
