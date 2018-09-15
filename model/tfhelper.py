import tensorflow as tf


def create_weights(shape):
    """
    tf.truncated_normal: return truncated random values.

    :param shape:
    :return:
    """

    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    """
    tf.constant: constant variable of 0.05 as initailized.
    :param size:
    :return:
    """
    return tf.Variable(tf.constant(0.05, shape=[size]))



