from google_images_download import google_images_download
import os
os.chdir("Background")
download_instance = google_images_download.googleimagesdownload()

arguments = \
    {"keywords":"Office,patterns,logos,home,design,artificial",
     "limit": 150,
     "chromedriver":r"C:\bin\chromedriver.exe",
     "size":">800*600",
     "format":"jpg",
     "print_urls":True}   #creating list of arguments

absolute_image_paths = download_instance.download(arguments)
print(absolute_image_paths)   #printing absolute paths of the downloaded images