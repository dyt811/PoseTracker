from image_prep import overlay
from PythonUtils.file import unique_name
from PythonUtils.folder import get_abspath
from background.bg_grabber import downloadGoogleImages
from specifiations.config import configuration
import os
import sys
import logging
from image_prep.overlay import subfolder as overlay_subfolder
from augmentation.augmentation_sequence import MarkerAug, CombinedAug
from augmentation.augmentation import subfolder as augment_subfolder
from image_prep.extract import crop_folder_bg

from image_prep.overlay import subfolder_random
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("CombinationModule")

def download(config):
    """
    Download the entire list of images based on the parameters defined.
    :param config: the configuration for pathing.
    :return:
    """

    download_specs = \
        {"keywords": "office,logos,home,environment,nature",
         "limit": 10,
         "chromedriver": r"C:\bin\chromedriver.exe",
         "size": ">6MP",
         "format": "jpg",
         "print_urls": True}   # creating list of download_specs

    bg_list = downloadGoogleImages(download_specs, config.bg)

def prepare_training_data():
    """
    Download, crop, foreground, augment the markers on a series of images.
    :returns: 1. Augmented folder with marker, 2. Control folder without marker.
    """


    root_folder = get_abspath(os.path.realpath(__file__), 2)
    paths = configuration(root_folder)
    download_files_delete = True
    download_files  = True
    augment_marker  = True
    augment_bg      = True
    augment_control = True

    # Some predefined folders if we are not redoing steps.
    crop_folder = r"C:\GitHub\MarkerTrainer\data_bg\cropped\2018-09-30T15_25_37.420490_500x500crop_downloads"
    control_folder = r"C:\GitHub\MarkerTrainer\data_bg\cropped\2018-09-30T15_25_45.436899_500x500crop_downloads"
    aug_markers = r"E:\Gitlab\MarkerTrainer\augmented_data\Marker\2018-09-22T12_40_28.641438500px"
    aug_bg = r"E:\Gitlab\MarkerTrainer\augmented_data\Bg\2018-09-22T13_01_52.483939500px"
    aug_bg_control = r"E:\Gitlab\MarkerTrainer\augmented_data\Bg\2018-09-22T12_41_09.122966500px"


    if download_files_delete and os.path.exists(paths.download):
        import shutil
        shutil.rmtree(paths.download)


    if download_files:
        # Download bg.
        download(paths)

        # Crop bgs
        crop_folder = crop_folder_bg(paths.download, paths.cropped, 500, 500)  # with over added soon
        control_folder = crop_folder_bg(paths.download, paths.cropped, 500, 500)  # server as control group

    # Augmented Marker
    if augment_marker:
        aug_markers = augment_subfolder(paths.folder_foreground_prime, paths.aug_fg, MarkerAug(), 2, "500px")

    # Augmented bg
    if augment_bg:
        aug_bg = augment_subfolder(crop_folder, paths.aug_bg, MarkerAug(), 1, "500px")

    # Augmented bg used as control
    if augment_control:
        aug_bg_control = augment_subfolder(control_folder, paths.aug_bg, MarkerAug(), 1, "500px")

    # Overlay augmented marker on cropped background.
    overlaid_cropped_folder = overlay_subfolder(aug_markers, aug_bg, paths.combined)

    # Augment the overlaid images.
    augmented_folder = augment_subfolder(overlaid_cropped_folder, paths.aug_merged, CombinedAug(), 1, "500px")

    # Augmented the background one more time.
    final_aug_bg = augment_subfolder(aug_bg_control, paths.aug_merged,CombinedAug(), 1,"500px")

    return augmented_folder, final_aug_bg


if __name__ == "__main__":
    #crop_bg(500, 500)
    #overlay_marker("C:\GitHub\MarkerTrainer\data_overlay\Prime", "C:\GitHub\MarkerTrainer\data_overlay\Background\cropped","C:\GitHub\MarkerTrainer\data_overlay\combined")
    #prepare_training_data()


    root_folder = get_abspath(os.path.realpath(__file__), 2)
    paths = configuration(root_folder)
    #subfolder_random(r"C:\GitHub\MarkerTrainer\data_augmented\bg\2018-09-30T16_53_53.984546500px", r"C:\GitHub\MarkerTrainer\data_augmented\marker\2018-09-30T16_51_35.374138500px", paths.folder_merged,50)

    aug_markers = augment_subfolder(paths.folder_foreground_prime, paths.aug_fg, MarkerAug(), 50, "500px")

