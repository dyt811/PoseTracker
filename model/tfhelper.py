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
    tf.constant:
    :param size:
    :return:
    """
    return tf.Variable(tf.constant(0.05, shape=[size]))


def show_progress(session, accuracy, epoch, feed_dict_train, feed_dict_validate, val_loss):
    acc = session.run(accuracy, feed_dict=feed_dict_train)
    val_acc = session.run(accuracy, feed_dict=feed_dict_validate)
    msg = "Training Epoch {0} --- Training Accuracy: {1:>6.1%}, Validation Accuracy: {2:>6.1%},  Validation Loss: {3:.3f}"
    print(msg.format(epoch + 1, acc, val_acc, val_loss))


