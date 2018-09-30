from PythonUtils.file import unique_name
from augmentation.augmentation_sequence import MarkerAug
import imageio
import os
import shutil
from foreground.load_batch import from_folder
from tqdm import tqdm
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def save_images(images_aug_collection, out_path):

    for image in images_aug_collection:
        # import matplotlib.pyplot as plt
        # plt.imshow(image, aspect="auto")
        # plt.show()

        filename = os.path.join(out_path, unique_name() + ".png")
        print(filename)
        # Saving the file.
        imageio.imwrite(filename, image)


def ImageAugmentator(image_path, out_path, aug_seq, iterations):
    '''
    Augment ONE image over ITERATIONS and output to the path, with the augmentation sequence given.
    :param image_path:
    :param out_path:
    :param aug_seq:
    :param iterations:
    :return:
    '''

    # Duplicate the images x times.
    for x in range(0, iterations):
        new_file_name = os.path.join(out_path, unique_name() + ".png")
        shutil.copyfile(image_path, new_file_name)

    folder(out_path, out_path, aug_seq, 1)


def subfolder(input_path, output_path, aug_sequence, iterations, aug_description):
    """
    A wrapped version of FolderAugmentator that create a UNQIUE subfolder.
    :param input_path: input path that contain the list of files.
    :param output_path: output root path, a
    :param aug_sequence: the augmentation seuqence that will be applied.
    :param iterations: number of the time to augment these input folders.
    :param aug_description: additional text string to be part of the folder name.
    :return: the path of the created SUBFOLDER
    """

    # Set and create the path of the augmented background.
    augmentation_folder = os.path.join(output_path, unique_name() + aug_description)
    os.makedirs(augmentation_folder)

    # Augment from input folder into the output folder.
    folder(input_path, augmentation_folder, aug_sequence, iterations)

    # return the path.
    return augmentation_folder

def folder(input_folder_path, out_path, aug_seg, iterations):
    """
    Duplicate the entire folder X iterations before augmenting the entire folder, using the augmentation sequence provided over the number of times requests.
    :param input_folder_path:
    :param out_path:
    :param aug_seg:
    :param iterations:
    :return:
    """

    # Generate temporary directory.
    #with TemporaryDirectory() as temporary_path:
    input_files = os.listdir(input_folder_path)

    # Duplicate the folder x times
    for x in tqdm(range(0, iterations)):
        os.chdir(input_folder_path)

        # each time, duplicate all the files within it
        for file in input_files:

            # Make sure to assign UNIQUE name.
            new_file_name = os.path.join(out_path, unique_name() + ".png")
            shutil.copyfile(file, new_file_name)

    logger.info("Augmenting from folder:" + out_path)

    # Load images into a giant matrices from the TEMP folder
    images_ndarray = from_folder(out_path)

    # Now that all images are in memory, time to delete all these "source" input files.
    shutil.rmtree(out_path)
    os.makedirs(out_path)

    # Augment the giant matrices
    images_augmented = aug_seg.augment_images(images_ndarray)

    logger.info("Saving augmenting images to: " + out_path)

    # Save the augmented images out to path.
    save_images(images_augmented, out_path)


if __name__ == "__main__":

    # Get the right augmentation sequence.
    aug_seq = MarkerAug()

    # Load Prime images.
    ImageAugmentator(r"E:\Gitlab\MarkerTrainer\overlay_data\Prime\100.png", r"E:\GitHub\MarkerTrainer\overlay_data\Altered", aug_seq, 10)