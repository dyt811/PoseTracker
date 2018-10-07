import os
import numpy as np
from imageio import imread

def from_filelist(file_list):
    """
    Load image data from a file lists given.
    :param path:
    :return:
    """
    # Data array to store the final image data information.
    data = []

    for file in file_list:
        try:
            # Read the image, add it to numpy array. Append it to data object to be returned in the end.
            img = imread(file)
            im = np.array(img)
            data.append(im)
        except Exception:
            # Regardless of what happens, continue and process next file, this is a batch information. CANNOT bes topped by any bad files.
            continue
    return data

def from_folder(path):
    """
    Load a batch of images from a folder.
    :param path:
    :return:
    """
    file_list = os.listdir(path)
    data = from_filelist(file_list)
    return data

if __name__ == "__main__":
    from_folder("Prime/")