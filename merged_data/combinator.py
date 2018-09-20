from ImageCropper.extract import crop_folder_bg
from ImageFuser import overlay
from PythonUtils.file import unique_name
from PythonUtils.folder import get_abspath
from bg_data.bg_grabber import downloadGoogleImages
import os

import logging

logger = logging.getLogger("CombinationModule")
from Specifiations.config import configuration




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
            overlay.randomly(bg, marker, new_file_name)
            logger.info("Generated " + new_file_name)



def download(config):
    """
    Download the entire list of images based on the parameters defined.
    :param config: the configuration for pathing.
    :return:
    """


    download_specs = \
        {"keywords": "black,black%20color,Office,patterns,logos,home,design,man-made",
         "limit": 5,
         "chromedriver": r"C:\bin\chromedriver.exe",
         "size": ">800*600",
         "format": "jpg",
         "print_urls": True}   # creating list of download_specs

    bg_list = downloadGoogleImages(download_specs, config.bg)


def augment(input_path, output_path, aug_sequence, aug_description):
    """

    :param aug_sequence: the augmentation seuqence that will be applied.
    :return:
    """
    from marker_data.img_aug import FolderAugmentator

    # Set and create the path of the augmented background.
    augmentation_bg_folder = os.path.join(output_path, unique_name() + aug_description)
    os.makedirs(augmentation_bg_folder)
    FolderAugmentator(input_path, augmentation_bg_folder, aug_sequence, 5)


def doEverything():

    # Download bg.
    root_folder = get_abspath(os.path.realpath(__file__), 2)
    path_config = configuration(root_folder)

    download(path_config)

    # Crop bgs
    from ImageCropper.extract import crop_folder_bg
    crop_folder1 = crop_folder_bg(path_config.download, path_config.cropped, 500, 500)  # with over added soon

    crop_folder2 = crop_folder_bg(path_config.download, path_config.cropped, 500, 500)  # server as control group

    # Overlay PRIME on cropped BG.
    from ImageFuser.overlay import overlay_subfolder
    overlaid_cropped_folder = overlay_subfolder(crop_folder1, path_config.prime, path_config.combined)

    # Set and create the path of the augmented prime
    augmentation_prime_folder = os.path.join(path_config.marker_aug, unique_name() + "500px")
    os.makedirs(augmentation_prime_folder)

    # Set and create the path of the combined augmented.
    combined_path = os.path.join(path_config.combined, os.path.basename(augmentation_bg_folder) + "+" + os.path.basename(augmentation_prime_folder))
    os.makedirs(combined_path)



    # Augment bgs

    from marker_data.augmentation_sequence import BackgroundAug500px
    augment(crop_folder1, path_config.bg_aug, BackgroundAug500px(),  "500px")


    # Augment prime
    FolderAugmentator(path_config.prime, augmentation_prime_folder, augmentation_sequences, 5)



def crop(config):
    """
    Crop ALL the images in the downloaded folder.
    :param config: the confirugration pathing indicating where to obtain the files.
    :return:
    """


if __name__ == "__main__":
    #crop_bg(500, 500)
    #overlay_marker("C:\GitHub\MarkerTrainer\marker_data\Prime", "C:\GitHub\MarkerTrainer\marker_data\Background\cropped","C:\GitHub\MarkerTrainer\marker_data\combined")
    doEverything()
