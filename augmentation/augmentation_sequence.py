from imgaug import augmenters as iaa

def Aug100px():
    """
    Augment 100 pixel images.
    :return:
    """
    aug_seq = iaa.Sequential([
        #iaa.Crop(px=(0, 15)),                                           # crop images from each side by 0 to 33px (randomly chosen)
        iaa.Fliplr(0.5),                                                # horizontally flip 50% of the images
        iaa.Flipud(0.5),  # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 2.0)),                               # blur images with a sigma of 0 to 2.0
        iaa.Multiply((0.25, 1.75), per_channel=True),
        iaa.AddToHueAndSaturation((-25, 25)),
        iaa.Dropout((0.01, 0.2), per_channel=True),
        iaa.SaltAndPepper((0.01,0.05), per_channel=True),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scale images to 80-120% of their size, individually per axis
            #translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
            rotate=(-45, 45),  # rotate by -45 to +45 degrees
            shear=(-16, 16),  # shear by -16 to +16 degrees
        )
    ])

    return aug_seq

def Aug200px():
    """
    Augment 200 pixel images.
    :return:
    """
    aug_seq = iaa.Sequential([
        #iaa.Crop(px=(0, 15)),                                           # crop images from each side by 0 to 33px (randomly chosen)
        iaa.Fliplr(0.5),                                                # horizontally flip 50% of the images
        iaa.Flipud(0.5),  # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 2.0)),                               # blur images with a sigma of 0 to 2.0
        iaa.Multiply((0.25, 1.75), per_channel=True),
        iaa.AddToHueAndSaturation((-25, 25)),
        iaa.Dropout((0.01, 0.2), per_channel=True),
        iaa.SaltAndPepper((0.01,0.05), per_channel=True),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scale images to 80-120% of their size, individually per axis
            #translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
            rotate=(-45, 45),  # rotate by -45 to +45 degrees
            shear=(-16, 16),  # shear by -16 to +16 degrees
        )
    ])

    return aug_seq

def Aug300px():
    """
    Augment 300 pixel images.
    :return:
    """
    aug_seq = iaa.Sequential([
        #iaa.Crop(px=(0, 15)),                                           # crop images from each side by 0 to 33px (randomly chosen)
        iaa.Fliplr(0.5),                                                # horizontally flip 50% of the images
        iaa.Flipud(0.5),  # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 2.0)),                               # blur images with a sigma of 0 to 2.0
        iaa.Multiply((0.25, 1.75), per_channel=True),
        iaa.AddToHueAndSaturation((-25, 25)),
        iaa.Dropout((0.01, 0.2), per_channel=True),
        iaa.SaltAndPepper((0.01,0.05), per_channel=True),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scale images to 80-120% of their size, individually per axis
            #translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
            rotate=(-45, 45),  # rotate by -45 to +45 degrees
            shear=(-16, 16),  # shear by -16 to +16 degrees
        )
    ])

    return aug_seq

def Aug400px():
    """
    Augment 400 pixel images.
    :return:
    """
    aug_seq = iaa.Sequential([
        #iaa.Crop(px=(0, 15)),                                           # crop images from each side by 0 to 33px (randomly chosen)
        iaa.Fliplr(0.5),                                                # horizontally flip 50% of the images
        iaa.Flipud(0.5),  # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 2.0)),                               # blur images with a sigma of 0 to 2.0
        iaa.Multiply((0.25, 1.75), per_channel=True),
        iaa.AddToHueAndSaturation((-25, 25)),
        iaa.Dropout((0.01, 0.2), per_channel=True),
        iaa.SaltAndPepper((0.01,0.05), per_channel=True),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scale images to 80-120% of their size, individually per axis
            #translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
            rotate=(-45, 45),  # rotate by -45 to +45 degrees
            shear=(-16, 16),  # shear by -16 to +16 degrees
        )
    ])

    return aug_seq

def Aug500px():
    """
    Augment 500 pixel images.
    :return:
    """
    aug_seq = iaa.Sequential([
        #iaa.Crop(px=(0, 15)),                                           # crop images from each side by 0 to 33px (randomly chosen)
        iaa.Fliplr(0.5),                                                # horizontally flip 50% of the images
        iaa.Flipud(0.5),  # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 2.0)),                               # blur images with a sigma of 0 to 2.0
        iaa.Multiply((0.25, 1.75), per_channel=True),
        iaa.AddToHueAndSaturation((-25, 25)),
        iaa.Dropout((0.01, 0.2), per_channel=True),
        iaa.SaltAndPepper((0.01,0.05), per_channel=True),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scale images to 80-120% of their size, individually per axis
            #translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
            rotate=(-45, 45),  # rotate by -45 to +45 degrees
            shear=(-16, 16),  # shear by -16 to +16 degrees
        )
    ])

    return aug_seq

def MarkerAug():
    """
    Marker arugmentatio that does not include noise as that augmentation is applied much later.
    :return:
    """
    sometimes = lambda aug: iaa.Sometimes(0.8, aug)
    aug_seq = iaa.Sequential(
        [
            iaa.Fliplr(0.5),  # horizontally flip 50% of the images
            iaa.Flipud(0.5),  # horizontally flip 50% of the images
            iaa.PerspectiveTransform(scale=(0.01, 0.1)),
            iaa.Multiply((0.25, 1.75), per_channel=True),
            iaa.AddToHueAndSaturation((-25, 25)),
            iaa.Affine(
                scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                # scale images to 80-120% of their size, individually per axis
                # translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  # translate by -20 to +20 percent (per axis)
                rotate=(-180, 180),  # rotate by -45 to +45 degrees
                shear=(-16, 16),  # shear by -16 to +16 degrees
            )
        ]
    )


    return aug_seq

def CombinedAug():
    """
    Augment 500 pixel images.
    :return:
    """
    sometimes = lambda aug: iaa.Sometimes(0.5, aug)

    aug_seq = iaa.Sequential([
        sometimes(iaa.Fliplr(0.5)),                                                # horizontally flip 50% of the images
        sometimes(iaa.Flipud(0.5)),  # horizontally flip 50% of the images
        sometimes(iaa.GaussianBlur(sigma=(0, 1.0))),                               # blur images with a sigma of 0 to 2.0
        sometimes(iaa.Multiply((0.25, 1.75))),
        sometimes(iaa.AddToHueAndSaturation((-25, 25))),
        sometimes(iaa.Dropout((0.01, 0.2), per_channel=True)),
        sometimes(iaa.SaltAndPepper((0.01,0.05)))
        ])

    return aug_seq