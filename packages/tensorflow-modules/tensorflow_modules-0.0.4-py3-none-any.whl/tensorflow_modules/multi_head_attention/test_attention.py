from . import attention
import tensorflow as tf
import unittest


class TestAttention(unittest.TestCase):
    batch_size = 10
    num_heads = 8
    depth = 512

    def test_dimension(self):
        q = tf.random.uniform([self.batch_size, self.num_heads, 1, self.depth])
        k = tf.random.uniform([self.batch_size, self.num_heads, 2, self.depth])
        v = tf.random.uniform([self.batch_size, self.num_heads, 2, self.depth])

        output, attention_weights = attention.scaled_dot_product_attention(q, k, v)
        self.assertEqual([self.batch_size, self.num_heads, 1, self.depth], output.shape)
        self.assertEqual([self.batch_size, self.num_heads, 1, 2], attention_weights.shape)

    def test_padding_mask(self):
        q = tf.random.uniform([self.batch_size, self.num_heads, 1, self.depth])
        k = tf.random.uniform([self.batch_size, self.num_heads, 2, self.depth])
        v = tf.random.uniform([self.batch_size, self.num_heads, 2, self.depth])

        padding_mask = tf.random.uniform([self.batch_size, 1, 1, 2])

        output, attention_weights = attention.scaled_dot_product_attention(q, k, v, padding_mask)
        self.assertEqual([self.batch_size, self.num_heads, 1, self.depth], output.shape)
        self.assertEqual([self.batch_size, self.num_heads, 1, 2], attention_weights.shape)

    def test_look_ahead_mask(self):
        q = tf.random.uniform([self.batch_size, self.num_heads, 1, self.depth])
        k = tf.random.uniform([self.batch_size, self.num_heads, 2, self.depth])
        v = tf.random.uniform([self.batch_size, self.num_heads, 2, self.depth])

        look_ahead_mask = tf.random.uniform([1, 1])

        output, attention_weights = attention.scaled_dot_product_attention(q, k, v, look_ahead_mask)
        self.assertEqual([self.batch_size, self.num_heads, 1, self.depth], output.shape)
        self.assertEqual([self.batch_size, self.num_heads, 1, 2], attention_weights.shape)
