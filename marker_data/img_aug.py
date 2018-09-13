from PythonUtils.file import unique_name
from marker_data.augmentation_sequence import Aug100px
import imageio
import os
import shutil
from tempfile import TemporaryDirectory
from marker_data.load_batch import from_folder


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

    try:
        # Generate temporary directory.
        with TemporaryDirectory() as temporary_path:
            # Duplicate the images x times.
            for x in range(0, iterations):
                new_file_name = os.path.join(temporary_path, unique_name() + ".png")
                shutil.copyfile(image_path, new_file_name)

            FolderAugmentator(temporary_path, out_path, aug_seq, 1)
    except PermissionError:
        print("Completed. Temporary not removable currently.")
        # Will have a removal failure.


def FolderAugmentator(folder_path, out_path, aug_seg, iterations):
    """
    Augment the entire folder, using the augmentation sequence provided over the number of times requests.
    :param folder_path:
    :param out_path:
    :param aug_seg:
    :param iterations:
    :return:
    """

    # Generate temporary directory.
    with TemporaryDirectory() as temporary_path:
        input_files = os.listdir(folder_path);

        # Duplicate the folder x times
        for x in range(0, iterations):
            os.chdir(folder_path)
            # each time, duplicate all the files within it
            for file in input_files:
                new_file_name = os.path.join(temporary_path, unique_name() + ".png")
                shutil.copyfile(file, new_file_name)

        # Load images into a giant matrices from the TEMP folder
        images_ndarray = from_folder(temporary_path)

        # Augment the giant matrices
        images_augmented = aug_seg.augment_images(images_ndarray)

        # Save the augmented images out to path.
        save_images(images_augmented, out_path)


if __name__ == "__main__":

    # Get the right augmentation sequence.
    aug_seq = Aug100px()

    # Load Prime images.
    ImageAugmentator(r"C:\GitHub\MarkerTrainer\marker_data\Prime\100.png", r"C:\GitHub\MarkerTrainer\marker_data\Altered", aug_seq, 100)