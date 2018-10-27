from generator.PoseDataSequence import DataSequence
import imghdr, os
import csv, json
from PythonUtils.file import read_json

def generate_csv(folder_path, csv_path):
    """
    Given a path to a folder with images, and their JSON files, output a CSV of:
     1) all the valid images where markers were detected.
     2) all the JSON files with .ROI.json is present.
     3) parse the JSON and file path into the CSV.
    :param folder_path:
    :param csv_path:
    :return:
    """
    from PythonUtils.folder import recursive_list
    file_list = recursive_list(folder_path)
    accepted_extensions=('png', 'jpg', 'gif', 'jpeg', 'tif', 'bmp')

    # Open files for writing.
    with open(csv_path, "w", newline='') as csv_file:

        # Open file
        csv_writer = csv.DictWriter(csv_file, fieldnames=["r1", "r2", "r0", "t1", "t2", "t0", "file"])
        csv_writer.writeheader()

        for file in file_list:
            # Header image header name.
            image_format = imghdr.what(file)

            # Check if they are anticipated.
            if image_format not in accepted_extensions:
                continue # skip file if image format is not compatible.

            # Check if JSON file exist.
            anticipated_JSON = file + ".ROI.json"
            if not os.path.exists(anticipated_JSON):
                continue # skip file if no JSON

            # Load JSON
            json_dictionary = read_json(anticipated_JSON)
            pose = json_dictionary.get("RelativePose")
            pose['file'] = file


            # Write to CSV
            csv_writer.writerow(pose)

    return csv_path

def delete_not_recognized_images(folder_path):
    """
    WARNING: DESTRUCTIVE FUNCTION. Use with care.
    Given a path, it will check if images has a marker recognized. If not, it will delete the images. This is mainly used
    to clean up the raw data input stream so that only images with paired JSON files will be sent off for machine learning trainings.

    :param folder_path: the path to the folder to carry out this operation.
    :return:
    """
    from PythonUtils.folder import recursive_list
    file_list = recursive_list(folder_path)
    accepted_extensions=('png', 'jpg', 'gif', 'jpeg', 'tif', 'bmp')


    for file in file_list:
        # Header image header name.
        image_format = imghdr.what(file)

        # Check if they are anticipated.
        if image_format not in accepted_extensions:
            continue # skip file if image format is not compatible.

        # Check if JSON file exist.
        anticipated_JSON = file + ".ROI.json"
        if not os.path.exists(anticipated_JSON):
            os.remove(file)



def generate_train_sequence(csv_path):
    training_sequence = DataSequence(csv_path, 100, mode="Train")
    return training_sequence
    # model.fit_generator(sequence, epochs=1, use_multiprocessing=True)

if __name__ == "__main__":
    generate_csv(r"C:\Yang\Dropbox\Machine_Learning\Recordings", r"C:\Temp\test_output.csv")