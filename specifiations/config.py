import os
from collections import namedtuple
from PythonUtils.folder import recursive_list

class configuration(object):

    def __init__(self, root_folder):

        # Section 1 on background
        # Set background data folder
        self.folder_background = os.path.join(root_folder, "data_bg")
        # Set Sub-background data folder
        self.folder_background_downloaded = os.path.join(self.folder_background, "downloads")
        self.folder_background_cropped = os.path.join(self.folder_background, "cropped")

        # Section 2 on foreground
        # Set marker data folder
        self.folder_foreground = os.path.join(root_folder, "data_overlay")

        # Set prime marker subfolder
        self.folder_foreground = os.path.join(root_folder, "foreground")
        self.folder_foreground_prime = os.path.join(self.folder_foreground, "Prime")

        # Section 3 on merged
        # Set combined output folder.
        self.folder_merged = os.path.join(root_folder, "data_merged")

        # Section 4 on augmentation
        # Set Augmented ouptut based on combined.
        self.folder_augmented = os.path.join(root_folder, "data_augmented")
        # Set Augmented prime marker
        self.folder_foreground_aug = os.path.join(self.folder_augmented, "marker")
        # Set Augmented bg
        self.folder_background_aug = os.path.join(self.folder_augmented, "bg")
        # Set Augmented merged
        self.folder_merged_aug = os.path.join(self.folder_augmented, "merged")

    @property
    def bg(self):
        """
        aboslute path to the bg folder
        :return:
        """
        return self.folder_background

    @property
    def download(self):
        """
        path: return the path to the download folder
        files: returns all the list of the files within that root folder.
        """
        return self.folder_background_downloaded

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
        return self.folder_background_cropped

    @property
    def marker(self):
        """
        absolute path to the root folder of all marker related data
        :return:
        """
        return self.folder_foreground_prime

    @property
    def foreground(self):
        """
        aboslute path to the prime folder which contains all the prototypical marker to be trained.
        :return:
        """
        return self.folder_foreground

    @property
    def combined(self):
        """
        absolute root path to the combined folder
        :return:
        """
        return self.folder_merged

    @property
    def aug_fg(self):
        """
        return the agumented foreground path.
        :return:
        """
        return self.folder_foreground_aug

    @property
    def aug_bg(self):
        """
        return the agumented foreground path.
        :return:
        """
        return self.folder_background_aug

    @property
    def aug_merged(self):
        """
        return the agumented foreground path.
        :return:
        """
        return self.folder_merged_aug