import os
import numpy as np
from imageio import imread



def from_folder(path):


    data = []
    for file in os.listdir(path):
        pathname = os.path.join(path, file)
        img = imread(pathname)
        im = np.array(img)
        data.append(im)
    return data

if __name__ == "__main__":
    from_folder("Prime/")