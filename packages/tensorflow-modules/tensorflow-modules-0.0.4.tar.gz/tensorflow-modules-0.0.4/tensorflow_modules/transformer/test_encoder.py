from . import encoder
import tensorflow as tf
import unittest


class TestEncoder(unittest.TestCase):
    d_model = 512
    num_heads = 8
    dff = 2048

    def test_dimension(self):
        model = encoder.Encoder(self.d_model, self.num_heads, self.dff)
        x = tf.random.uniform([64, 43, 512])

        output = model(x, False, None)
        self.assertEqual([64, 43, 512], output.shape.as_list())
