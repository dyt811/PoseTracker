from PythonUtils.folder import recursive_list
from PIL import Image
from tqdm import tqdm
files = recursive_list(r"C:\Yang\Dropbox\Machine_Learning\orientation_validation")
for file in tqdm(files):
    try:
        if "ROI" in file:
            continue
        im = Image.open(file)
        width, height = im.size   # Get dimensions
        new_width = 480;
        left = (width - new_width)/2
        right = (width + new_width)/2
        new_im = im.crop((left, 0, right, height))
        new_im.save(file,"BMP")
    except:
        continue
