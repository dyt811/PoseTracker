from imgaug import augmenters as iaa
from datetime import datetime
from marker_data.load_batch import from_folder

import imageio
import os
import shutil
import tempfile
import time
from tempfile import TemporaryDirectory
from marker_data.load_batch import from_folder

def Aug100px():
    """
    Augment 100 pixel images.
    :return:
    """
    aug_seq = iaa.Sequential([
        #iaa.Crop(px=(0, 15)),                                           # crop images from each side by 0 to 33px (randomly chosen)
        iaa.Fliplr(0.5),                                                # horizontally flip 50% of the images
        iaa.Flipud(0.5),  # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 2.0)),                               # blur images with a sigma of 0 to 2.0
        iaa.Multiply((0.25, 1.75), per_channel=True),
        iaa.AddToHueAndSaturation((-25, 25)),
        iaa.Dropout((0.01, 0.2), per_channel=True),
        iaa.SaltAndPepper((0.01,0.05), per_channel=True),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scale images to 80-120% of their size, individually per axis
            #translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
            rotate=(-45, 45),  # rotate by -45 to +45 degrees
            shear=(-16, 16),  # shear by -16 to +16 degrees
        )
    ])

    return aug_seq


def unique_name():
    timestamp = datetime.now().isoformat(sep='T', timespec='auto')
    name = timestamp.replace(":", "_")
    return name


def save_images(images_aug_collection, out_path):

    for image in images_aug_collection:
        # import matplotlib.pyplot as plt
        # plt.imshow(image, aspect="auto")
        # plt.show()

        filename = os.path.join(out_path, unique_name() + ".png")
        print(filename)
        # Saving the file.
        imageio.imwrite(filename, image)


def singleImageAugmentator(image_path, out_path, aug_seq, iterations):

    try:
        # Generate temporary directory.
        with TemporaryDirectory() as temporary_path:
            # Duplicate the images x times.
            for x in range(0, iterations):
                new_file_name = os.path.join(temporary_path, unique_name() + ".png")
                shutil.copyfile(image_path, new_file_name)

            singleFolderAugmentator(temporary_path, out_path, aug_seq, 1)
    except PermissionError:
        print("Completed. Temporary not removable currently.")
        # Will have a removal failure.

def singleFolderAugmentator(folder_path, out_path, aug_seg, iterations):

    # Generate temporary directory.
    with TemporaryDirectory() as temporary_path:
        # Duplicate the folder x times
        for x in range(0, iterations):
            os.chdir(folder_path)
            # each time, duplicate all the files within it
            for file in os.listdir(folder_path):
                new_file_name = os.path.join(temporary_path, unique_name() + ".png")
                shutil.copyfile(file, new_file_name)

        # Load images into a giant matrices from the TEMP folder
        images_ndarray = from_folder(temporary_path)

        # Augment the giant matrices
        images_augmented = aug_seg.augment_images(images_ndarray)

        # Save the augmented images out to path.
        save_images(images_augmented, out_path)


if __name__ == "__main__":

    # Get the right augmentation sequence.
    aug_seq = Aug100px()

    # Load Prime images.
    singleImageAugmentator(r"C:\GitHub\MarkerTrainer\marker_data\Prime\100.png", r"C:\GitHub\MarkerTrainer\marker_data\Altered", aug_seq, 100)