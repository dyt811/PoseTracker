import os
from PIL import Image
import random
from tqdm import tqdm

def overlay(image_bg, image_overlay, alpha):




    image_bg = image_bg.convert("RGBA")
    image_overlay = image_overlay.convert("RGBA")

    new_img = Image.blend(image_bg, image_overlay, alpha)
    return new_img


def randomly(image_bg_path, image_overlay_path, output):
    """
    Over lay an image on top of the background image, and output it to certain location
    :param image_bg_path:
    :param image_overlay_path:
    :param output:
    :return:
    """

    # suppose img1 and img2 are your two images
    bg = Image.open(image_bg_path)
    bg_width, bg_height = bg.size

    overlay = Image.open(image_overlay_path)
    overlay_width, overlay_height = overlay.size

    if overlay_width > bg_width or overlay_height > bg_height:
        return None

    #Coordinate calculation:
    paste_wide_boundary = bg_width - overlay_width
    paste_height_boundary = bg_height - overlay_height
    random_paste_width = int(random.uniform(0, paste_wide_boundary))
    random_paste_height = int(random.uniform(0, paste_height_boundary))

    bg.paste(overlay, (random_paste_width, random_paste_height))
    bg.show()

    #new_img = overlay(bg, overlay, alpha)
    bg.save(output, "PNG")

def overlay_subfolder(bg_folder, overlay_folder, output_root_path):
    """
    Wrapper function that output to a UNIQUE subfolder instead of directly into the folder. For output into a SPECIFIC output folder, use the overlay_folder instead.
    :param bg_folder:
    :param overlay_folder:
    :param output_root_path:
    :return:
    """

    from PythonUtils.file import unique_name
    unique_path = output_root_path + unique_name()
    os.makedirs(unique_path)
    overlay_folder(bg_folder, overlay_folder, output_root_path)
    return unique_path

def overlay_folder(bg_folder, overlay_folder, output_path):
    """
    Output the combinatino of BG and OVERLAY into a TARGET folder.
    :param bg_folder:
    :param overlay_folder:
    :param output_path:
    :return:
    """

    for bg in tqdm(bg_folder):
        for overlay in tqdm(overlay_folder):
            randomly(bg, overlay, output_path)


if __name__ == "__main__":
    randomly("../a.jpg", "../b.JPG", 0.1, "new.jpg")