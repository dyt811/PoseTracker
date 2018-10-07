from PIL import Image
import random
import os
from PythonUtils.file import unique_name, duplicates_into_folders
from PythonUtils.folder import recursive_list
import logging
import sys
from tqdm import tqdm
import shutil

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
"""
This class explores the images and crop out as many smaller conforming image section as possible. 
"""

def area(image, x, y, width, height):
    """
    Crop and image using the given coordinate based on the width and height given.
    :param image:
    :param x:
    :param y:
    :param width:
    :param height:
    :return:
    """
    img = Image.open(image)
    area = (x, y, x+width, y+height)
    cropped_img = img.crop(area)
    #cropped_img.show()
    return cropped_img


def randomly(image, width, height):
    """
    Randomly crop areas of the image that is equivalent to the given width and height.
    :param image:
    :param width:
    :param height:
    :return:
    """
    img = Image.open(image)
    img_width, img_height = img.size

    crop_wide_boundary = img_width - width
    crop_height_boundary = img_height - height
    if crop_height_boundary < 0 or crop_wide_boundary < 0:
        return None
    random_crop_x = int(random.uniform(0, crop_wide_boundary))
    random_crop_y = int(random.uniform(0, crop_height_boundary))

    return area(image, random_crop_x, random_crop_y, width, height)

def crop_filelist(filelist, output_folder, width, height, iterations):
    """
    crop the background images and generate the cropped version of them that are only 500x500
    :param image_folder: folder contain downloads.
    :param width: width of the area will be cropped out.
    :param height: height of the area will be cropped out.
    :return:
    """

    # Duplicate input file lists X iterations into the output destination
    updated_filelist = duplicates_into_folders(filelist,output_folder, iterations)

    # For all the files, try to convert and export to that address
    for file in tqdm(updated_filelist):
        try:
            image_path = file
            image = randomly(image_path, width, height)
        except OSError:
            logger.info("Found a bad file. Ignoring: " + file)
            continue

        bg_cropped_path = os.path.join(output_folder, unique_name() + ".png")

        if image is None:
            continue
        else:
            try:
                # Generate a RGB image from the cropped image. This FORCE the image to be RGB even if it was originally GRAY scale!
                rgbimg = Image.new("RGBA", image.size)

                # Paste the image in.
                rgbimg.paste(image)

                # Save the file.
                rgbimg.save(bg_cropped_path, "PNG")
                logger.info("Saved " + bg_cropped_path)

                # Delete the original
                os.remove(file)
            except OSError:
                logger.info("Found a bad file. Ignoring: " + file + " from " + image_path)
                continue


def crop_folder(image_folder, output_folder, width, height, iterations):
    """
    crop the background images and generate the cropped version of them that are only 500x500
    :param image_folder: folder contain downloads.
    :param output_folder: folder where all the output will be dumped into
    :param width: width of the area will be cropped out.
    :param height: height of the area will be cropped out.
    :return:
    """
    # Change into the directory
    # List all the relevant folders.
    files = recursive_list(image_folder)

    # Make DIR if it does not already exist.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    crop_filelist(files, output_folder, width, height, iterations)


def crop_folder_bg(input_image_root_folder, output_root_folder, width, height, iterations):
    """
    A batch function for cropping the background images and generate the cropped version of them that are only 500x500
    :param input_image_root_folder: folder contain downloads.
    :param width: width of the area will be cropped out.
    :param height: height of the area will be cropped out.
    :return:
    """
    # Generate the temp name that will be used to store the crop results.
    crop_folder_name = unique_name() + "_" + str(width) + "x" + str(height)

    # Combine folder and root to form path name.
    output_subfolder = os.path.join(output_root_folder, crop_folder_name)

    # Make DIR if it does not already exist.
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    crop_folder(input_image_root_folder, output_subfolder, width, height, iterations)

    return output_subfolder

if __name__ == "__main__":
    #randomly("../a.jpg", 400, 400)
    crop_folder_bg(r"E:\Gitlab\MarkerTrainer\bg_data\background\\", 400, 400)