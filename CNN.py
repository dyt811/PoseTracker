import tensorflow as tf
import model.tflayers as tfl
from model.dataset import read_train_sets
import logging
from numpy.random import seed
from tensorflow import set_random_seed

# Source inspired from "https://cv-tricks.com/Tensorflow-tutorials/tutorial-2-image-classifier/train.py"

logger = logging.getLogger(__name__)

# Declaration of the classes:
classes = ['marker', 'no-marker']
num_classes = len(classes)



# Path of the training data folder
train_path = r'E:\Gitlab\MarkerTrainer\data_training'

# Validation proportion
validation_size = 0.333333

# Batch size
batch_size = 8

# Image related properties
num_channels = 3    # color chanels?
image_size = 500    # in pixel

# Read the training data set into a DataSets class object.
data = read_train_sets(train_path, image_size, classes, validation_size=validation_size)


print("Complete reading input data. Will Now print a snippet of it")
print("Number of files in Training-set:\t\t{}".format(len(data.train.labels)))
print("Number of files in Validation-set:\t{}".format(len(data.valid.labels)))


"""
Random seed initialization
"""
#Adding Seed so that random initialization is consistent
seed(1)
set_random_seed(2)


"""
Instantian the session
"""
session = tf.Session()


"""
Placeholder functions for input/output
"""



# TF PLACEHOLDER: Declare where the INPUT images data will be fed
# NONE is the batch size?
x = tf.placeholder(tf.float32, shape=[None, image_size, image_size, num_channels], name='x')

# TF PLACEHOLDER: Declare where the INPUT label data will be fed
# NONE is the batch size?
y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')

# Returns the index with the largest value across axes of a tensor. So, class?
y_true_cls = tf.argmax(y_true, dimension=1)



"""
Network Graph Parameters. 
"""

# Layer Paramemters:
L1_filter = 128
L1_convSize = 3

L2_filter = 64
L2_convSize = 3

L3_filter = 32
L3_convSize = 3

L4_filter = 16
L4_convSize = 3

L5_filter = 8
L5_convSize = 3

L6_filter = 4
L6_convSize = 3

L7_filter = 2
L7_convSize = 3

FC1_size = 64


"""
Building Network. 
"""

# Building the ConvolutionLayers
conv_stack1 = tfl.create_convolutional_stack(input              = x,
                                             num_input_channels = num_channels,
                                             conv_filter_size   = L1_convSize,
                                             num_filters        = L1_filter)

conv_stack2 = tfl.create_convolutional_stack(input              = conv_stack1,
                                             num_input_channels = L1_filter,
                                             conv_filter_size   = L2_convSize,
                                             num_filters        = L2_filter)

conv_stack3 = tfl.create_convolutional_stack(input              = conv_stack2,
                                             num_input_channels  = L2_filter,
                                             conv_filter_size   = L3_convSize,
                                             num_filters        = L3_filter)

conv_stack4 = tfl.create_convolutional_stack(input              = conv_stack3,
                                             num_input_channels = L3_filter,
                                             conv_filter_size   = L4_convSize,
                                             num_filters        = L4_filter)

conv_stack5 = tfl.create_convolutional_stack(input              = conv_stack4,
                                             num_input_channels  = L4_filter,
                                             conv_filter_size   = L5_convSize,
                                             num_filters        = L5_filter)

conv_stack6 = tfl.create_convolutional_stack(input              = conv_stack5,
                                             num_input_channels = L5_filter,
                                             conv_filter_size   = L6_convSize,
                                             num_filters        = L6_filter)

conv_stack7 = tfl.create_convolutional_stack(input              = conv_stack6,
                                             num_input_channels  = L6_filter,
                                             conv_filter_size   = L7_convSize,
                                             num_filters        = L7_filter)


# Building the Flat Layers
layer_flat = tfl.create_flatten_layer(conv_stack7)

# Building the Fully Connected Layers
fc_stack1 = tfl.create_fc_stack(input       = layer_flat,
                                num_inputs  = layer_flat.get_shape()[1:4].num_elements(),
                                num_outputs = FC1_size,
                                use_relu    = True)

fc_stack2 = tfl.create_fc_stack(input       = fc_stack1,
                                num_inputs  = FC1_size,
                                num_outputs = num_classes,
                                use_relu    = False)



# Generate prediction using a softmax layer
y_pred = tf.nn.softmax(fc_stack2, name="y_pred")

# Generate the classification of the prediction class
y_pred_cls = tf.argmax(y_pred, dimension=1)


# Initailize the session and all variables.
session.run(tf.global_variables_initializer())



"""
LOSS FUNCTION
"""

# Use cross-entropy with logits as the LOSS function against the GROUND TRUTH
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=fc_stack2, labels=y_true)

# Cost converted.
cost = tf.reduce_mean(cross_entropy)

# Optimizer
optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cost)

# Count the number of the correct predictions
correct_prediction = tf.equal(y_pred_cls, y_true_cls)

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

session.run(tf.global_variables_initializer())

total_iterations = 0

saver = tf.train.Saver()


def show_progress(epoch, feed_dict_train, feed_dict_validate, val_loss):
    acc = session.run(accuracy, feed_dict=feed_dict_train)
    val_acc = session.run(accuracy, feed_dict=feed_dict_validate)
    msg = "Training Epoch {0} --- Training Accuracy: {1:>6.1%}, Validation Accuracy: {2:>6.1%},  Validation Loss: {3:.3f}"
    print(msg.format(epoch + 1, acc, val_acc, val_loss))


def train(num_iteration):
    global total_iterations

    for i in range(total_iterations,
                   total_iterations + num_iteration):

        x_batch, y_true_batch, _, cls_batch = data.train.next_batch(batch_size)
        x_valid_batch, y_valid_batch, _, valid_cls_batch = data.valid.next_batch(batch_size)

        feed_dict_tr = {x: x_batch,
                        y_true: y_true_batch}
        feed_dict_val = {x: x_valid_batch,
                         y_true: y_valid_batch}

        session.run(optimizer, feed_dict=feed_dict_tr)

        if i % int(data.train.num_examples / batch_size) == 0:
            val_loss = session.run(cost, feed_dict=feed_dict_val)
            epoch = int(i / int(data.train.num_examples / batch_size))

            show_progress(epoch, feed_dict_tr, feed_dict_val, val_loss)
            saver.save(session, 'dogs-cats-model')

    total_iterations += num_iteration


train(num_iteration=30)