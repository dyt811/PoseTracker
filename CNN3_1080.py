from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.layers import LeakyReLU
import keras
import os
from PythonUtils.file import unique_name, filelist_delete, recursive_list

from generator.PoseDataSequence import DataSequence
from generator.csvgen import generate_csv
from PythonUtils.folder import get_abspath
from dotenv import load_dotenv

def cleanLog(input_path):
    if input_path is None:
        # Dynamicly generate model input_path.
        project_root = os.path.realpath(__file__)
        log_path = os.path.join(os.path.dirname(project_root), "logs")
    else:
        log_path = input_path

    if os.path.exists(log_path):
        files = recursive_list(log_path)
        if len(files) > 0:
            filelist_delete(files)

def load_data_and_run(model,input_shape, TBCallBack):
    load_dotenv()
    train_path          = os.getenv("train_path")
    train_csv_path      = os.getenv("train_csv_path")
    validate_path       = os.getenv("validate_path")
    validate_csv_path   = os.getenv("validate_csv_path")

    # Dynamicly generate model path.
    project_root = os.path.realpath(__file__)
    model_path = os.path.join(os.path.dirname(project_root), "models")

    generate_csv(train_path, train_csv_path )
    train_data = DataSequence(train_csv_path, 100, mode="Train")

    generate_csv(validate_path,validate_csv_path)
    validation_data = DataSequence(validate_csv_path, 100)

    model_name = os.path.join(model_path, unique_name())

    checkpoint = ModelCheckpoint(model_name, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [TBCallBack, checkpoint]

    model.fit_generator(
            train_data,
            steps_per_epoch=100,
            epochs=50,
            validation_data=validation_data,
            validation_steps=100,
            callbacks=callbacks_list
    )
    model.save(os.path.join(model_path, unique_name()))

def createModel(input_shape, output_classes):
    model = Sequential()
    model.add(Conv2D(16, (5, 5), padding='same', strides=(2,2), input_shape=(input_shape, input_shape, 3)))
    model.add(LeakyReLU(alpha=0.1))
    #model.add(Conv2D(16, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(16, (3, 3), padding='same', strides=(1,1)))
    model.add(LeakyReLU(alpha=0.1))
    #model.add(Conv2D(32, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    # model.add(Conv2D(32, (3, 3), padding='same', strides=(1,1)))
    # model.add(LeakyReLU(alpha=0.1))
    # #model.add(Conv2D(64, (5, 5), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.2))
    #
    # model.add(Conv2D(32, (3, 3), padding='same', strides=(1,1)))
    # model.add(LeakyReLU(alpha=0.1))
    # #model.add(Conv2D(64, (5, 5), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.2))
    #
    # model.add(Conv2D(64, (3, 3), padding='same', strides=(1,1)))
    # model.add(LeakyReLU(alpha=0.1))
    # #model.add(Conv2D(64, (5, 5), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.2))
    #
    # model.add(Conv2D(64, (3, 3), padding='same', strides=(1, 1)))
    # model.add(LeakyReLU(alpha=0.1))
    # # model.add(Conv2D(64, (5, 5), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.5))
    model.add(Dense(output_classes))

    return model

if __name__ =="__main__":
    from time import time

    cleanLog(None)
    image_size = 480
    model1 = createModel(image_size, 3) # downsize to 128
    model1.compile(loss="sparse_categorical_crossentropy", optimizer="adadelta", metrics=["acc", "mae"])

    # Dynamicly generate model input_path.
    project_root = os.path.realpath(__file__)
    log_path = os.path.join(os.path.dirname(project_root), "logs")

    tensorboard = keras.callbacks.TensorBoard(
        log_dir=log_path,
        histogram_freq=0,
        write_images=True)

    load_data_and_run(model1, image_size, tensorboard)