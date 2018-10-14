from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.layers import LeakyReLU
import keras
import os
from PythonUtils.file import unique_name, filelist_delete, recursive_list

def cleanLog(path=r"E:\Gitlab\MarkerTrainer\logs"):
    if os.path.exists(path):
        files = recursive_list(path)
        if len(files) > 0:
            filelist_delete(files)

def load_data_and_run(model,input_shape, TBCallBack):
    train_data_loader = ImageDataGenerator(samplewise_center=True, samplewise_std_normalization=True)
    train_data = train_data_loader.flow_from_directory(r"E:\Gitlab\MarkerTrainer\data_train",
                                                       target_size=(input_shape,input_shape),
                                                       batch_size=128,
                                                       color_mode="grayscale",
                                                       class_mode='binary')

    validation_data_loader = ImageDataGenerator(samplewise_center=True, samplewise_std_normalization=True)
    validation_data = validation_data_loader.flow_from_directory(r"E:\Gitlab\MarkerTrainer\data_validate",
                                                       target_size=(input_shape, input_shape),
                                                       batch_size=128,
                                                       color_mode="grayscale",
                                                       class_mode='binary')
    model_name = os.path.join(r"E:\Gitlab\MarkerTrainer\models", unique_name())

    checkpoint = ModelCheckpoint(model_name, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [TBCallBack, checkpoint]

    model.fit_generator(
            train_data,
            steps_per_epoch=100,
            epochs=20,
            validation_data=validation_data,
            validation_steps=100,
            callbacks=callbacks_list
    )
    model.save(os.path.join(r'E:\Gitlab\MarkerTrainer\models\\', unique_name()))

def createModel(input_shape, output_classes):
    model = Sequential()
    model.add(Conv2D(16, (3, 3), padding='same', strides=(2,2), input_shape=(input_shape, input_shape, 1)))
    model.add(LeakyReLU(alpha=0.1))
    #model.add(Conv2D(16, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(16, (3, 3), padding='same', strides=(1,1)))
    model.add(LeakyReLU(alpha=0.1))
    #model.add(Conv2D(32, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(32, (3, 3), padding='same', strides=(1,1)))
    model.add(LeakyReLU(alpha=0.1))
    #model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(32, (3, 3), padding='same', strides=(1, 1)))
    model.add(LeakyReLU(alpha=0.1))
    # model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3), padding='same', strides=(1, 1)))
    model.add(LeakyReLU(alpha=0.1))
    # model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.5))
    model.add(Dense(output_classes))
    model.add(Activation('softmax'))

    # Param: 276138

    return model

if __name__ =="__main__":
    from time import time

    cleanLog()
    image_size = 250
    model1 = createModel(image_size, 2) # downsize to 128
    model1.compile(loss="sparse_categorical_crossentropy", optimizer="adadelta", metrics=["acc", "mae"])

    tensorboard = keras.callbacks.TensorBoard(
        log_dir=r'E:\Gitlab\MarkerTrainer\logs',
        histogram_freq=0,
        write_images=True)

    load_data_and_run(model1, image_size, tensorboard)