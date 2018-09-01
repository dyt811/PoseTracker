from ImageCropper import extract
from ImageFuser import overlay
from oshelper.filehelper import unique_name

import os

import logging

logger = logging.getLogger("CombinationModule")

def crop_bg():

    # This is the folder where all downloads actually go into.
    image_folder_root = os.path.join(os.getcwd(), r"Background\downloads")

    # Change into the directory
    os.chdir(image_folder_root)

    # List all the relevant folders.
    downloaded_image_folders = list(
        filter(os.path.isdir, os.listdir(image_folder_root))
    )

    # Loop through each folder,
    for folder_path in downloaded_image_folders:

        # Combine root image folder with the specific folder, go into it.
        final_path = os.path.join(image_folder_root, folder_path)

        os.chdir(final_path)

        folder = str(final_path)

        # replaced downloads with CROPPED in the folder path.
        cropped_folder = folder.replace("downloads", "cropped")

        # Make DIR if it does not already exist.
        if not os.path.exists(cropped_folder):
            os.makedirs(cropped_folder)

        files = [f for f in os.listdir('.') if os.path.isfile(f)]

        for file in files:

            os.chdir(folder)

            try:
                image = extract.randomly(os.path.join(folder,file), 500, 500)
            except OSError:
                print("Found a bad file. Ignoring: " + file + " from " + folder)
                continue

            file_name = file.replace(" ", "_")

            bg_cropped = os.path.join(cropped_folder, file_name)

            if image is None:
                continue
            else:
                image.save(bg_cropped, "PNG")
                print("Saved ", bg_cropped)

def overlay_marker(marker_folder, bg_folder, combined_folder):
    """
    Combine markers and folders together to form the training data set.
    :param marker_folder:
    :param bg_folder:
    :return:
    """
    for marker in marker_folder:
        for bg in bg_folder:
            new_file_name = os.path.join(combined_folder,unique_name())
            overlay.randomly(bg, marker, 0.5, new_file_name)
            logger.info("Generated " + new_file_name)


if __name__ == "__main__":
    crop_bg()
    overlay_marker("C:\GitHub\MarkerTrainer\marker_data\Prime", "C:\GitHub\MarkerTrainer\marker_data\Background\cropped", "C:\GitHub\MarkerTrainer\marker_data\Combined")
