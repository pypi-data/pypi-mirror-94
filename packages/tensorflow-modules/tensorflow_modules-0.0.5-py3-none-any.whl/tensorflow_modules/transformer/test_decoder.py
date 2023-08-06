from . import decoder
import tensorflow as tf
import unittest


class TestEncoder(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048

    def test_dimension(self):
        model = decoder.Decoder(self.d_model, self.num_heads, self.dff)
        x = tf.random.uniform([64, 43, 512])
        enc_output = tf.random.uniform([64, 43, 512])

        output, attn1, attn2 = model(x, enc_output, False, None, None)
        self.assertEqual([64, 43, 512], output.shape.as_list())
        self.assertEqual([64, 8, 43, 43], attn1.shape)
        self.assertEqual([64, 8, 43, 43], attn2.shape)
