import tensorflow as tf


class PointWiseFeedForwardNetwork(tf.keras.layers.Layer):
    def __init__(self, d_model, dff):
        super(PointWiseFeedForwardNetwork, self).__init__()

        self.ffn = tf.keras.Sequential([
            tf.keras.layers.Dense(dff, activation='relu'),  # (batch_size, seq_len, dff)
            tf.keras.layers.Dense(d_model)                  # (batch_size, seq_len, d_model)
        ])

    def call(self, x):
        return self.ffn(x)
