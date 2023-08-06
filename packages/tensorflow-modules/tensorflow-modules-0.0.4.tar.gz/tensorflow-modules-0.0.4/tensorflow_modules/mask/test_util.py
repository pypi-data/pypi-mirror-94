from . import util
import tensorflow as tf
import unittest


class TestMask(unittest.TestCase):
    def test_create_padding_mask(self):
        seq = tf.random.uniform([3, 5])

        mask = util.create_padding_mask(seq)
        self.assertEqual([3, 1, 1, 5], mask.shape)

    def test_create_padding_mask2(self):
        seq = tf.random.uniform([3, 4, 5])

        mask = util.create_padding_mask(seq)
        self.assertEqual([3, 1, 1, 4, 5], mask.shape)

    def test_create_look_ahead_mask(self):
        mask = util.create_look_ahead_mask(5)
        self.assertEqual([5, 5], mask.shape)
