import tensorflow as tf


def create_padding_mask(seq):
    seq = tf.cast(tf.math.equal(seq, 0), tf.float32)

    # アテンション・ロジットにパディングを追加するため
    # さらに次元を追加する
    return seq[:, tf.newaxis, tf.newaxis, :]    # (batch_size, 1, 1, seq_len)


def create_look_ahead_mask(size):
    return 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)    # (seq_len, seq_len)
