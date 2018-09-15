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

    bg_folder = os.path.join(root_folder, "bg_data")
    downloaded_folder = os.path.join(bg_folder, "downloads")
    cropped_folder = os.path.join(bg_folder, "cropped")
    augmented_bg = os.path.join(bg_folder, "augmented")



    marker_folder = os.path.join(root_folder, "marker_data")
    prime = os.path.join(marker_folder, "Prime")
    augmented_marker = os.path.join(marker_folder, "augmented")

    combined_folder = os.path.join(root_folder, "merged_data")

    download_specs = \
        {"keywords": "black,black%20color,Office,patterns,logos,home,design,man-made",
         "limit": 5,
         "chromedriver": r"C:\bin\chromedriver.exe",
         "size": ">800*600",
         "format": "jpg",
         "print_urls": True}   # creating list of download_specs

    bg_list = downloadGoogleImages(download_specs, bg_folder)


    # Crop bgs
    from ImageCropper.extract import crop_folder_bg
    crop_folder1 = crop_folder_bg(downloaded_folder, cropped_folder, 500, 500)  # with over added soon
    crop_folder2 = crop_folder_bg(downloaded_folder, cropped_folder, 500, 500)  # server as control group

    # Augment bgs
    from marker_data.img_aug import FolderAugmentator
    from marker_data.augmentation_sequence import BackgroundAug500px

    # Set augmentation parameters
    augmentation_sequences = BackgroundAug500px()

    # Set and create the path of the augmented background.
    augmentation_bg_folder = os.path.join(augmented_bg, unique_name() + "500px")
    os.makedirs(augmentation_bg_folder)
    FolderAugmentator(crop_folder1, augmentation_bg_folder, augmentation_sequences, 5)


    # Set and create the path of the augmented prime.
    augmentation_prime_folder = os.path.join(augmented_marker, unique_name() + "500px")
    os.makedirs(augmentation_prime_folder)
    # Augment prime
    FolderAugmentator(prime, augmentation_prime_folder, augmentation_sequences, 5)

    # Set and create the path of the combined augmented.
    combined_path = os.path.join(combined_folder, os.path.basename(augmentation_bg_folder) + "+" + os.path.basename(augmentation_prime_folder))
    os.makedirs(combined_path)

    # Merge those two folders to generate the final data.
    from ImageFuser.overlay import overlay_folder_random
    overlay_folder_random(augmentation_bg_folder, augmentation_prime_folder, combined_path)

if __name__ == "__main__":
    #crop_bg(500, 500)
    #overlay_marker("C:\GitHub\MarkerTrainer\marker_data\Prime", "C:\GitHub\MarkerTrainer\marker_data\Background\cropped","C:\GitHub\MarkerTrainer\marker_data\combined")
    doEverything()
