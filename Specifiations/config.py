import os
from collections import namedtuple
from PythonUtils.folder import recursive_list

class configuration(object):

    def __init__(self, root_folder):
        pass

        # Section 1 on BG
        # Set background data folder
        self.bg_folder = os.path.join(root_folder, "data_bg")
        # Set Sub-background data folder
        self.downloaded_folder = os.path.join(self.bg_folder, "downloads")
        self.cropped_folder = os.path.join(self.bg_folder, "cropped")

        # Section 2 on Marker
        # Set marker data folder
        self.overlay_folder = os.path.join(root_folder, "data_overlay")
        # Set prime marker subfolder
        self.prime_overlay = os.path.join(self.overlay_folder, "Prime")

        # Section 3 on Combination
        # Set combined output folder.
        self.combined_folder = os.path.join(root_folder, "data_merged")

        # Section 4 on Augmentation
        # Set Augmented ouptut based on combined.
        self.augmented_folder = os.path.join(root_folder, "data_augmented")

        # Set Augmented prime marker
        self.overlay_aug_folder = os.path.join(self.augmented_folder, "Marker")

        # Set Augmented bg
        self.bg_aug_folder = os.path.join(self.augmented_folder, "Bg")

        # Set Augmented merged
        self.merged_aug_folder = os.path.join(self.augmented_folder, "Merged")

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
        return self.downloaded_folder

    @property
    def download_files(self):
        """
        return a list of all downloaded files in the download folder.
        :return:
        """
        from PythonUtils.folder import recursive_list
        file_list = recursive_list(self.download)
        return file_list

    @property
    def cropped(self):
        """
        absolute path to the cropped background data root folder
        :return:
        """
        return self.cropped_folder

    @property
    def marker(self):
        """
        absolute path to the root folder of all marker related data
        :return:
        """
        return self.overlay_folder

    @property
    def overlay(self):
        """
        aboslute path to the prime folder which contains all the prototypical marker to be trained.
        :return:
        """
        return self.prime_overlay

    @property
    def combined(self):
        """
        absolute root path to the combined folder
        :return:
        """
        return self.combined_folder

    @property
    def aug_overlay(self):
        """
        return the agumented overlay path.
        :return:
        """
        return self.overlay_aug_folder

    @property
    def aug_bg(self):
        """
        return the agumented overlay path.
        :return:
        """
        return self.bg_aug_folder

    @property
    def aug_merged(self):
        """
        return the agumented overlay path.
        :return:
        """
        return self.merged_aug_folder