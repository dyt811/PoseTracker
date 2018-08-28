from imgaug import augmenters as iaa
from datetime import datetime
import matplotlib.pyplot as plt
import imageio
import os

if __name__ == "__main__":



    seq = iaa.Sequential([
        iaa.Crop(px=(0, 33)), # crop images from each side by 0 to 16px (randomly chosen)
        #iaa.Fliplr(0.5), # horizontally flip 50% of the images
        #iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
    ])

    from marker_data.load_batch import from_folder

    images = from_folder("Prime/")

    images_aug = seq.augment_images(images)

    for image in images_aug:




        plt.imshow(image, aspect="auto")
        plt.show()
        # Convert to PIL format from NDNUMPY
        # im = Image.fromarray(numpy.uint8(image))


        timestamp = datetime.now().isoformat(sep='T', timespec='auto')
        name = timestamp.replace(":", "_")
        filename = os.path.join("Altered", name + ".png")
        print(filename)
        # Saving the file.
        imageio.imwrite(filename, image)

    # for batch_idx in range(100):
    #     # 'images' should be either a 4D numpy array of shape (N, height, width, channels)
    #     # or a list of 3D numpy arrays, each having shape (height, width, channels).
    #     # Grayscale images must have shape (height, width, 1) each.
    #     # All images must have numpy's dtype uint8. Values are expected to be in
    #     # range 0-255.
    #     images = load_batch(batch_idx)
    #     images_aug = seq.augment_images(images)

