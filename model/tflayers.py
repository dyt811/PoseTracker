import tensorflow as tf
from model.tfhelper import create_weights, create_biases

#Source: https://cv-tricks.com/tensorflow-tutorial/training-convolutional-neural-network-for-image-classification/

def create_convolutional_stack(input,
                               num_input_channels,
                               conv_filter_size,
                               num_filters):
    """
    A wrapper for tf.nn.conv2d that generate Conv2d stack with:
        layer
        bias
        maxpool
        relu activation

    :param input:
    :param num_input_channels:
    :param conv_filter_size:
    :param num_filters:
    :return:
    """
    # We shall define the weights that will be trained using create_weights function.
    weights = create_weights(shape=[conv_filter_size, conv_filter_size, num_input_channels, num_filters])

    # We create biases using the create_biases function. These are also trained.
    biases = create_biases(num_filters)

    # Creating the convolutional layer
    layer = tf.nn.conv2d(input=input,
                         filter=weights,
                         strides=[1, 1, 1, 1],
                         padding='SAME')

    layer += biases

    # We shall be using max-pooling.
    layer = tf.nn.max_pool(value=layer,
                           ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1],
                           padding='SAME')
    # Output of pooling is fed to Relu which is the activation function for us.
    layer = tf.nn.relu(layer)

    return layer


def create_flatten_layer(layer):
    """
    tf reshape the input layer to a flattened layer
    :param layer:
    :return:
    """
    layer_shape = layer.get_shape()
    num_features = layer_shape[1:4].num_elements()
    layer = tf.reshape(layer, [-1, num_features])

    return layer


def create_fc_stack(input,
                    num_inputs,
                    num_outputs,
                    use_relu=True):
    """

    :param input:
    :param num_inputs:
    :param num_outputs:
    :param use_relu:
    :return:
    """
    # Let's define trainable weights and biases.
    weights = create_weights(shape=[num_inputs, num_outputs])
    biases = create_biases(num_outputs)

    # Multiply the INPUT and WEIGHT matrix then add BIAS
    layer = tf.matmul(input, weights) + biases

    # Activate the Layer via RELU.
    if use_relu:
        layer = tf.nn.relu(layer)

    return layer
