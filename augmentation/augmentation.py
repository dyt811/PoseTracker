import sys
print(sys.path)
from PythonUtils.file import unique_name, filelist_delete, duplicates_into_folders
from PythonUtils.folder import recursive_list
import imageio
import os
import shutil
from foreground.load_batch import from_folder, from_filelist
from tqdm import tqdm, trange
import copy
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def save_images(images_aug_collection, out_path):
    """
    Take an augmented image collection an a path, then iterate through the collection to save them.
    :param images_aug_collection: the data bundle that has been properly augmented
    :param out_path: the output ROOT path where all images will reside.
    :return:
    """
    for image in tqdm(images_aug_collection):
        # import matplotlib.pyplot as plt
        # plt.imshow(image, aspect="auto")
        # plt.show()

        # Generate the time stamp required.
        filename = os.path.join(out_path, unique_name() + ".png")

        logger.info("Saving" + filename)

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
    It does a batch augmentation process per 1000 images because memory cannot load that many more at the same time.
    :param input_folder_path:
    :param out_path:
    :param aug_seg:
    :param iterations:
    :return:
    """

    input_files = recursive_list(input_folder_path)

    # Duplicate the folder X times.
    input_augment_files = duplicates_into_folders(input_files, out_path, iterations)

    logger.info("Augmenting files from folder:" + out_path)

    # Decide if to do batch augmentation or all augmentation.
    with trange(len(input_augment_files)) as pbar:

        while len(input_augment_files) != 0:
            # While the files to be processed < 1000, just read the damn thing.
            if len(input_augment_files) < 1000:
                processing_data = copy.deepcopy(input_augment_files) # Assign all remaining items to processing data.
                input_augment_files.clear() # Empty the list to trigger exit condition.

            # When there are more files, we actually try to process 1k images at a time, augment, write out. then.
            else:
                # Transfer the top of the list to another variable.
                processing_data = input_augment_files[0:999]

                # Truncate original list.
                del input_augment_files[0:999]

            #COMMON PORTION. Previous section only modify the input_augment_files list and what needs to be processed.
            # Load images into a giant matrices from the TEMP folder
            images_ndarray = from_filelist(processing_data)

            # Now that all images are in memory, time to delete all these "source" input files.
            filelist_delete(processing_data)

            # Augment the giant matrices
            images_augmented = aug_seg.augment_images(images_ndarray)

            logger.info("Saving augmenting images to: " + out_path)

            # Save the augmented images out to path.
            save_images(images_augmented, out_path)

            # Update progress bar of the augmentation
            pbar.update(len(input_augment_files))
        pbar.close()
        logger.info("All images augmented.")


# When launching main, the path of the python is set to execute from THIS particular directory and will have trouble recognizing higher level as packages.
if __name__ == "__main__":
    from augmentation_sequence import MarkerAug
    # Get the right augmentation sequence.
    aug_seq = MarkerAug()

    # Load Prime images.
    # ImageAugmentator(r"E:\Gitlab\MarkerTrainer\overlay_data\Prime\100.png", r"E:\GitHub\MarkerTrainer\overlay_data\Altered", aug_seq, 10)

    folder(r"E:\Gitlab\MarkerTrainer\foreground\Prime", r"C:\temp\AugMarker", aug_seq, 10000)