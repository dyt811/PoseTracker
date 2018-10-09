import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import numpy as np

batch size = 128
num_classes = 2
epochs = 12

# input image dimensions
img_rows, img_cols = 500, 500
channels = 3
fashion_mnist = keras.datasets.fashion_mnist

# Data split:
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

x_train = x_train.reshape(300, img_rows, img_cols, 1)
x_test = x_test.rehapse(300,img_rows, img_cols,1 )


# Binary class matrix: y = [0, 1] would be no-marker when the classes are [marker, no-marker]
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(filters=32,
                 kernel_size=(3,3),
                 activation='relu',
                 input_shape=(500,500,1)))
model.add(MaxPooling2D(pool_size=(2,2),
                       strides=2))
model.add(Conv2D(filters=32,
                 kernel_size=(3,3),
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2),
                       strides=2))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.adam,
              metric=['accuracy']
              )
model.fit(x_train,y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test,y_test))
score=model.evaluat(x_test,y_test,verbose=0)
print('Test loss:', score[0])
print('Test accurayc:', score[1])