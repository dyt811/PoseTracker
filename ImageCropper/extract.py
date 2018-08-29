from PIL import Image
import random

"""
This class explores the images and crop out as many smaller conforming image section as possible. 
"""

def area(image, x, y, width, height):
    img = Image.open(image)
    area = (x, y, x+width, y+height)
    cropped_img = img.crop(area)
    cropped_img.show()
    return cropped_img

def randomly(image, width, height):
    img = Image.open(image)
    img_width, img_height = img.size

    crop_wide_boundary = img_width - width
    crop_height_boundary = img_height - height

    random_crop_x = int(random.uniform(0, crop_wide_boundary))
    random_crop_y = int(random.uniform(0, crop_height_boundary))

    return area(image, random_crop_x, random_crop_y, width, height)

if __name__ == "__main__":
    randomly("../a.jpg", 400, 400)