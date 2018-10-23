from keras.utils import Sequence
from keras.preprocessing.image import load_img
import pandas as pd
import numpy as np
import random
import math

class DataSequence(Sequence):
    """
    A customary sequence class to help obtain the input necessary for training.
    """

    def __init__(self, csv_path, batch_size, mode='train'):

        # read the csv file with pandas
        self.df = pd.read_csv(csv_path)

        # batch size
        self.bsz = batch_size

        # shuffle when in train mode
        self.mode = mode

        # CSV files should have the following headers:
        # x, y, z, w, p, r, file

        # Take labels and a list of image locations in memory
        self.labels = self.df[['r1', 'r2', 'r0']].values # THIS IS Y
        self.im_list = self.df['file'].tolist()

    def __len__(self):
        # compute number of batches to yield
        return int(math.ceil(len(self.df) / float(self.bsz)))

    def on_epoch_end(self):
        # Shuffles indexes after each epoch if in training mode
        self.indexes = range(len(self.im_list))
        if self.mode == 'train':
            self.indexes = random.sample(self.indexes, k=len(self.indexes))

    def get_batch_labels(self, idx):
        # Fetch a batch of labels
        return self.labels[idx * self.bsz: (idx + 1) * self.bsz,:]

    def get_batch_features(self, idx):
        # Fetch a batch of inputs
        return np.array([load_img(im) for im in self.im_list[idx * self.bsz: (1 + idx) * self.bsz]])

    def __getitem__(self, idx):
        batch_x = self.get_batch_features(idx)
        batch_y = self.get_batch_labels(idx)
        return batch_x, batch_y
