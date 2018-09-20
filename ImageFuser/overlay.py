import os
from PIL import Image
import random
from tqdm import tqdm
from PythonUtils.file import unique_name
import logging
logger = logging.getLogger(__name__)



def overlay(image_bg, image_overlay, alpha):
    image_bg = image_bg.convert("RGBA")
    image_overlay = image_overlay.convert("RGBA")

    new_img = Image.blend(image_bg, image_overlay, alpha)
    return new_img


def randomly(bg_image_path, overlay_image_path, output_image_path):
    """
    Over lay an image on top of the background image, and output it to certain location
    :param bg_image_path:
    :param overlay_image_path:
    :param output_image_path:
    :return:
    """

    # suppose img1 and img2 are your two images
    bg = Image.open(bg_image_path)
    bg_width, bg_height = bg.size

    overlay = Image.open(overlay_image_path)
    overlay_width, overlay_height = overlay.size

    if overlay_width > bg_width or overlay_height > bg_height:
        return None

    #Coordinate calculation:
    paste_wide_boundary = bg_width - overlay_width
    paste_height_boundary = bg_height - overlay_height
    random_paste_width = int(random.uniform(0, paste_wide_boundary))
    random_paste_height = int(random.uniform(0, paste_height_boundary))

    bg.paste(overlay, (random_paste_width, random_paste_height))
    # bg.show()

    #new_img = overlay(bg, overlay, alpha)
    # New image name

    # file_name = os.path.join(output, unique_name() + os.path.basename(image_bg_path) + os.path.basename(image_overlay_path))

    bg.save(output_image_path, "PNG")


def subfolder(bg_folder, overlay_folder, output_root_path):
    """
    Wrapper function that output to a UNIQUE subfolder instead of directly into the folder. For output into a SPECIFIC output folder, use the overlay_folder instead.
    :param bg_folder:
    :param overlay_folder:
    :param output_root_path:
    :return:
    """
    unique_path = os.path.join(output_root_path, "Overlay_"+ unique_name() + os.path.basename(bg_folder) + "_" + os.path.basename(overlay_folder))
    os.makedirs(unique_path)
    folder(bg_folder, overlay_folder, unique_path)
    return unique_path


def folder(bg_folder, overlay_folder, output_path):
    """
    Output the combinatino of BG and OVERLAY into a TARGET folder.
    :param bg_folder:
    :param overlay_folder:
    :param output_path:
    :return:
    """
    from PythonUtils.folder import recursive_list
    bg_list = recursive_list(bg_folder)
    overlay_list = recursive_list(overlay_folder)

    for bg_image in tqdm(bg_list):
        for overlay_image in overlay_list:
            try:
                randomly(bg_image, overlay_image, output_path)
            except FileNotFoundError:
                logger.info(bg_image)
                continue


if __name__ == "__main__":
    randomly("../a.jpg", "../b.JPG", 0.1, "new.jpg")