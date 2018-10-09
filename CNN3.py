from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard
import keras
import os
from PythonUtils.file import unique_name
def load_data_and_run(model,input_shape, TBCallBack):
    train_data_loader = ImageDataGenerator()
    train_data = train_data_loader.flow_from_directory(r"E:\Gitlab\MarkerTrainer\data_train",
                                                       target_size=(input_shape,input_shape),
                                                       batch_size=128,
                                                       class_mode='binary')
    validation_data_loader = ImageDataGenerator()
    validation_data = validation_data_loader.flow_from_directory(r"E:\Gitlab\MarkerTrainer\data_validate",
                                                       target_size=(input_shape, input_shape),
                                                       batch_size=128,
                                                       class_mode='binary')
    model.fit_generator(
            train_data,
            steps_per_epoch=2500,
            epochs=50,
            validation_data=validation_data,
            validation_steps=1250,
            #callbacks=TBCallBack
    )
    model.save(os.path.join(r'E:\Gitlab\MarkerTrainer\models\\', unique_name()))

def createModel(input_shape, output_classes):
    model = Sequential()
    model.add(Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=(input_shape, input_shape, 3)))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(output_classes))
    model.add(Activation('softmax'))

    # Param: 276138

    return model

if __name__ =="__main__":
    from time import time
    model1 = createModel(128, 2) # downsize to 128
    model1.compile(loss="sparse_categorical_crossentropy", optimizer="adam")
    TBCallBack = TensorBoard(log_dir=r'E:\Gitlab\MarkerTrainer\logs',
                                             histogram_freq=0,
                                             batch_size=32,
                                             write_graph=True,
                                             write_grads=True,
                                             write_images=True,
                                             embeddings_freq=0,
                                             embeddings_layer_names=None,
                                             embeddings_metadata=None,
                                             embeddings_data=None,
                                             update_freq='epoch')

    load_data_and_run(model1, 128, TBCallBack)