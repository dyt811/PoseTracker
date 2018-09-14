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
train_path = 'merged_data/'

# Validation proportion
validation_size = 0.2

# Batch size
batch_size = 32

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
L1_filter = 32
L1_convSize = 3

L2_filter = 32
L2_convSize = 3

L3_filter = 64
L3_convSize = 3

FC1_size = 128


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

# Building the Flat Layers
layer_flat = tfl.create_flatten_layer(conv_stack3)

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



train(num_iteration=3000)