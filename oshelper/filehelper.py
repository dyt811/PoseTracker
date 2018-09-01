import datetime
import os

def unique_name():
    timestamp = datetime.now().isoformat(sep='T', timespec='auto')
    name = timestamp.replace(":", "_")
    return name

def recursively_list_folder(root_dicom_path):
    """
    load all the files, validate and then pass to decompress or anonimize.
    :param root_dicom_path:
    :return:
    """
    global file_list
    file_list = []

    for root, directories, filenames in os.walk(root_dicom_path):
        #for directory in directories:
            #file_list.append(os.path.join(root, directory))
        for filename in filenames:
            file_list.append(os.path.join(root,filename))
    return file_list