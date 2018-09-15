import os
import numpy as np
from imageio import imread



def from_folder(path):
    """
    Load a batch of images from a folder.
    :param path:
    :return:
    """

    # Data array to store the final image data information.
    data = []


    for file in os.listdir(path):

        # Regenerate the full abbsolute path.
        pathname = os.path.join(path, file)

        # Read the image, add it to numpy array. Append it to data object to be returned in the end.
        img = imread(pathname)
        im = np.array(img)
        data.append(im)

    return data

if __name__ == "__main__":
    from_folder("Prime/")