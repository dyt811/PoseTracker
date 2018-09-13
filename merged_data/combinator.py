from ImageCropper.extract import crop_folder_bg
from ImageFuser import overlay
from PythonUtils.file import unique_name
from PythonUtils.folder import get_abspath
from bg_data.bg_grabber import downloadGoogleImages
import os

import logging

logger = logging.getLogger("CombinationModule")




def overlay_marker(marker_folder, bg_folder, combined_folder):
    """
    Combine markers and folders together to form the training data set.
    :param marker_folder: folders where markers images are replaced
    :param bg_folder: folders where patterns images are replaced
    :return:
    """
    for marker in marker_folder:
        for bg in bg_folder:
            new_file_name = os.path.join(combined_folder, unique_name())
            overlay.randomly(bg, marker, 0.5, new_file_name)
            logger.info("Generated " + new_file_name)

def doEverything():

    # Download bg.
    root_folder = get_abspath(os.path.realpath(__file__), 2)
    bg_folder = os.path.join(root_folder, "bg_data","background")
    arguments = \
        {"keywords": "Office,patterns,logos,home,design,man-made",
         "limit": 150,
         "chromedriver": r"C:\bin\chromedriver.exe",
         "size": ">800*600",
         "format": "jpg",
         "print_urls": True}   # creating list of arguments

    #bg_list = downloadGoogleImages(arguments, bg_folder)

    downloaded_folder = os.path.join(bg_folder, "downloads")

    # Crop bgs
    from ImageCropper.extract import crop_folder_bg
    crop_folder = crop_folder_bg(bg_folder, 500, 500)

    # Augment bgs
    from marker_data.img_aug import FolderAugmentator
    from marker_data.augmentation_sequence import BackgroundAug500px

    # Set augmentation parameters
    augmentation_sequences = BackgroundAug500px()

    # Set and create the path of the augmentation
    augmentation_folder = os.path.join(bg_folder, "Augmented", unique_name() + "_BackgroundAug500px")
    os.makedirs(augmentation_folder)

    # Augment into that.
    FolderAugmentator(crop_folder, augmentation_folder, augmentation_sequences, 5)

    # Grab prime.

    # Augment prime

    # Combine them to provide the training data set.
    merged_folder = os.path.join(root_folder, "merged_data", "")

if __name__ == "__main__":
    #crop_bg(500, 500)
    #overlay_marker("C:\GitHub\MarkerTrainer\marker_data\Prime", "C:\GitHub\MarkerTrainer\marker_data\Background\cropped","C:\GitHub\MarkerTrainer\marker_data\Combined")
    doEverything()
