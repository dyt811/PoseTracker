import os
from collections import namedtuple
from PythonUtils.folder import recursive_list

class configuration(object):

    def __init__(self, root_folder):
        pass

        # Set background data folder
        self.bg_folder = os.path.join(root_folder, "bg_data")

        # Set Sub-background data folder
        self.downloaded_folder = os.path.join(self.bg_folder, "downloads")
        self.cropped_folder = os.path.join(self.bg_folder, "cropped")

        # Set marker data folder
        self.marker_folder = os.path.join(root_folder, "marker_data")

        # Set prime marker subfolder
        self.prime = os.path.join(self.marker_folder, "Prime")

        # Set combined output folder.
        self.combined_folder = os.path.join(root_folder, "merged_data")

        # Set Augmented ouptut based on combined.
        self.augmented_folder = os.path.join(root_folder, "augmented_data")

    @property
    def bg(self):
        """
        aboslute path to the bg folder
        :return:
        """
        return self.bg_folder




    @property
    def download(self):
        """
        path: return the path to the download folder
        files: returns all the list of the files within that root folder.
        """


        download = namedtuple("path", "files")
        files = recursive_list(self.downloaded_folder)

        result = download(self.downloaded_folder, files)
        return result

    @property
    def download_files(self):

    @property
    def cropped(self):
        """
        absolute path to the cropped background data root folder
        :return:
        """
        return self.cropped_folder

    @property
    def bg_aug(self):
        """
        absolute path to the augmented, cropped background data root folder
        :return:
        """
        return self.augmented_bg

    @property
    def marker(self):
        """
        absolute path to the root folder of all marker related data
        :return:
        """
        return self.marker_folder

    @property
    def prime(self):
        """
        aboslute path to the prime folder which contains all the prototypical marker to be trained.
        :return:
        """
        return self.prime

    @property
    def marker_aug(self):
        """
        absolute root path to the markers that have already been augmented
        :return:
        """
        return self.augmented_marker

    @property
    def combined(self):
        """
        absolute root path to the combined folder
        :return:
        """
        return self.combined_folder
