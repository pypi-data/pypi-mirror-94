import tensorflow as tf
from tensorflow.python.keras import layers, regularizers
from rslib.algo.tensorflow.layers.interaction import BiInteractionPooling
# from rslib.algo.tensorflow.sparse_dnn.DenseLayerForSparse import DenseLayerForSparse
from rslib.algo.tensorflow.sparse_dnn.DenseLayerForSparse import DenseLayerForSparse


def id_input_processing(user_feature_input, config):
    '''
    处理 ID类 特征，
    使用 Embedding 对 ID类 特征进行嵌入，同时提供对特征的组合。
    目前支持的组合方式有 FM

    Args:
        user_feature_input: 输入
        config: 配置信息

    Returns:

    '''
    emb_size = config['emb_size']
    user_feature_size = config['user_feature_size']

    layers_emb_fm1_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=1, embeddings_regularizer=regularizers.l2(0.001))
    layers_emb_fm2_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=emb_size, embeddings_regularizer=regularizers.l2(0.001))
    layers_FM = BiInteractionPooling()

    user_feature_1 = layers.Flatten()(layers_emb_fm1_user_feature(user_feature_input))
    user_feature_2 = layers.Flatten()(layers_FM(layers_emb_fm2_user_feature(user_feature_input)))
    user_feature = layers.Concatenate(axis=1)([user_feature_1, user_feature_2])

    user_feature = layers.Dense(emb_size, activation='relu', kernel_regularizer=regularizers.l2(0.001))(user_feature)
    # user_feature = layers.Dense(emb_size, activation='sigmoid')(user_feature)
    # user_feature = layers.Dropout(0.5)(user_feature)
    return user_feature


def id_input_embe_processing(user_feature_input, config):
    '''
    处理 ID类 特征，
    使用 Embedding 对 ID类 特征进行嵌入

    Args:
        user_feature_input: 输入
        config: 配置信息

    Returns:

    '''
    emb_size = config['emb_size']
    user_feature_size = config['user_feature_size']

    layers_emb_fm2_user_feature = layers.Embedding(input_dim=user_feature_size, output_dim=emb_size)

    user_feature = layers_emb_fm2_user_feature(user_feature_input)

    return user_feature


def cross_input_processing(cross_feature_input, config):
    '''
    处理 稀疏特征，
    使用稀疏全连击网络对 稀疏 特征进行处理

    Args:
        cross_feature_input: 稀疏特征
        config: 配置信息

    Returns:

    '''
    activation = 'relu'
    hidden_unit = config['hidden_units']
    cross_feature_num = config['cross_feature_num']
    cross_feature = DenseLayerForSparse(cross_feature_num, hidden_unit, activation)(cross_feature_input)
    cross_feature = layers.Dense(hidden_unit, activation='relu')(cross_feature)
    cross_feature = layers.Dropout(0.2)(cross_feature)
    cross_feature = layers.Dense(hidden_unit, activation='relu')(cross_feature)
    cross_feature = layers.Dropout(0.2)(cross_feature)
    return cross_feature


def sequence_input_LSTM(sequence_id_input, config):
    '''
    处理 序列特征，
    使用 LSTM 模型对序列特征进行序列化处理

    Args:
        sequence_id_input: 序列特征
        config: 配置信息

    Returns:

    '''
    class_num = config['class_num']
    hidden_unit = config['hidden_units']
    emb_size = config['emb_size']
    seq_num = config['seq_num']

    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])

    seqs_lstm = []
    for i in range(seq_num):
        seq_i = seq_index_layer([sequence_id_input, i])
        seq_i_embeddings = layers.Embedding(class_num, emb_size, mask_zero=True)(seq_i)
        seq_i_lstm = layers.LSTM(units=hidden_unit)(seq_i_embeddings)
        seqs_lstm.append(seq_i_lstm)

    seqs_embeddings = layers.Concatenate(axis=-1)(seqs_lstm) if len(seqs_lstm) > 1 else seqs_lstm[0]

    return seqs_embeddings


def sequence_input_Transformer(sequence_id_input, config):
    '''
        处理 序列特征，
        使用 Transformer 模型对序列特征进行序列化处理

        Args:
            sequence_id_input: 序列特征
            config: 配置信息

        Returns:

    '''
    pass


def sequence_group_embedding(sequence_id_input, sequence_time_input, config):
    '''
        处理 序列特征，
        将序列特征分组，对每个组的序列特征分别处理，
        对每个时间步的特征分别做融合

        Args:
            sequence_id_input: 序列特征
            config: 配置信息

        Returns:

    '''
    hidden_unit = config['hidden_units']
    class_num = config['class_num']
    emb_size = config['emb_size']
    seq_num = config['seq_num']
    seq_group_index = config['seq_group']
    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])
    seq_class_num = config['seq_class_num']
    layers_emb_sequence_feature = [layers.Embedding(input_dim=class_num, output_dim=emb_size) for i, class_num in enumerate(seq_class_num)]

    # seq
    list_group_dense = []
    list_group_time_mask = []
    for seqs in seq_group_index:
        list_seq_emb = []
        for i in seqs:
            seq_i = seq_index_layer([sequence_id_input, i])
            emb_seq_i = layers_emb_sequence_feature[i](seq_i)
            list_seq_emb.append(emb_seq_i)

        emb_group_j = layers.Concatenate(axis=2)(list_seq_emb) if len(list_seq_emb) > 1 else list_seq_emb[0]
        dense_group_j = layers.Dense(hidden_unit, activation='relu')(emb_group_j)
        list_group_dense.append(dense_group_j)

        time_mask_group_j = seq_index_layer([sequence_time_input, seqs[0]])
        list_group_time_mask.append(time_mask_group_j)

    dense_all = layers.Concatenate(axis=1)(list_group_dense) if len(list_group_dense) > 1 else list_group_dense[0]
    dense_all = layers.Dense(hidden_unit, activation='relu')(dense_all)
    time_mask_all = layers.Concatenate(axis=1)(list_group_time_mask) if len(list_group_time_mask) > 1 else \
        list_group_time_mask[0]
    return dense_all, time_mask_all


def sequence_embedding(sequence_id_input, sequence_time_input, config):
    hidden_unit = config['hidden_units']
    class_num = config['class_num']
    emb_size = config['emb_size']
    seq_num = config['seq_num']
    seq_group_index = config['seq_group']
    seq_emb_type = config['seq_emb_type']

    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])
    layers_emb_sequence_feature = [layers.Embedding(input_dim=class_num, output_dim=emb_size) for _ in range(seq_num)]
    list_group_dense = []
    list_group_time_mask = []
    # seq_group_index=[[0]]
    for seqs in seq_group_index:
        for i in seqs:
            seq_i = seq_index_layer([sequence_id_input, i])
            emb_seq_i = layers_emb_sequence_feature[i](seq_i)
            list_group_dense.append(emb_seq_i)

        time_mask_group_j = seq_index_layer([sequence_time_input, seqs[0]])
        list_group_time_mask.append(time_mask_group_j)

    if seq_emb_type == 'add':
        dense_all = layers.add(list_group_dense) if len(list_group_dense) > 1 else list_group_dense[0]
        time_mask_all = list_group_time_mask[0]
    else:
        dense_all = layers.Concatenate(axis=-1)(list_group_dense) if len(list_group_dense) > 1 else list_group_dense[0]
        dense_all = layers.Dense(hidden_unit, activation='relu')(dense_all)
        time_mask_all = list_group_time_mask[0]
        # time_mask_all = layers.Concatenate(axis=1)(list_group_time_mask) if len(list_group_time_mask) > 1 else \
        #     list_group_time_mask[0]
    return dense_all, time_mask_all, list_group_dense


def sequence_tar_embedding(sequence_id_input, sequence_time_input, config, target_seq=None):
    hidden_unit = config['hidden_units']
    class_num = config['class_num']
    emb_size = config['emb_size']
    target_seq = config['target_seq'] if target_seq is None else target_seq

    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])
    layers_emb_sequence_feature = layers.Embedding(input_dim=class_num, output_dim=emb_size)
    # i
    list_seq_emb = []
    for i in target_seq:
        seq_i = seq_index_layer([sequence_id_input, i])
        emb_seq_i = layers_emb_sequence_feature(seq_i)
        list_seq_emb.append(emb_seq_i)

    emb_group_target = layers.Concatenate(axis=2)(list_seq_emb) if len(list_seq_emb) > 1 else list_seq_emb[0]

    # todo，将 sequence_tar 在 T 维度进行pooling，可以考虑使用其他的方式
    # emb_group_target = layers.Lambda(lambda x: tf.reduce_mean(x, 1, keep_dims=True))(emb_group_target)
    # dense_group_target = layers.Dense(hidden_unit,activation='relu')(emb_group_target)
    # time_mask_group_target = tf.ones([tf.shape(emb_group_target)[0], 1])

    dense_group_target = layers.Dense(hidden_unit, activation='relu')(emb_group_target)
    time_mask_group_target = seq_index_layer([sequence_time_input, target_seq[0]])

    return dense_group_target, time_mask_group_target
