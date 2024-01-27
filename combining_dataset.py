
# Importing all the required libraries
import os, sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

# gathering each of the seperate file paths to create a combined image dataset
OUTPUT_DIR = "D:/Deep learning/galaxy-image-classification-main/Final_dataset"
IMAGE_SIDE_SIZE = 128

INPUT_DIRS = {
    "elliptical" : "D:/Deep learning/galaxy-image-classification-main/elliptical",
    "spiral" : "D:/Deep learning/galaxy-image-classification-main/spiral",
    "irregular" : "D:/Deep learning/Irregular Galaxies/irregular_aug",
    "invalid" : "D:/Deep learning/Invalid dataset/invalid/invalid"
}

galaxy_npys = {
    "elliptical" : np.zeros((1, IMAGE_SIDE_SIZE, IMAGE_SIDE_SIZE, 3), dtype = np.uint8),
    "spiral" : np.zeros((1, IMAGE_SIDE_SIZE, IMAGE_SIDE_SIZE, 3), dtype = np.uint8),
    "irregular" : np.zeros((1, IMAGE_SIDE_SIZE, IMAGE_SIDE_SIZE, 3), dtype = np.uint8),
    "invalid" : np.zeros((1, IMAGE_SIDE_SIZE, IMAGE_SIDE_SIZE, 3), dtype = np.uint8)
}

# Getting the number of instances in each class
for galaxy_class in INPUT_DIRS.keys():
  print(galaxy_class, ":\t", len(os.listdir(INPUT_DIRS[galaxy_class])))

#combining all images of 4 classes into a single output path specified
counter = 0
for galaxy_class in INPUT_DIRS.keys():

  for image_name in os.listdir(INPUT_DIRS[galaxy_class]):
    if "jpg" in image_name:
      temp = cv2.imread(os.path.join(INPUT_DIRS[galaxy_class], image_name))
      temp = cv2.resize(temp, (IMAGE_SIDE_SIZE, IMAGE_SIDE_SIZE))

      temp = np.expand_dims(temp, axis = 0)
      galaxy_npys[galaxy_class] = np.concatenate((galaxy_npys[galaxy_class], temp[:]), axis = 0)
      ## create the output structure manually
      cv2.imwrite(os.path.join(OUTPUT_DIR, galaxy_class, image_name), temp)

      counter += 1
      
      if counter % 100 == 0:
        print(counter, "images done!")

print(counter, "images DONE!")

#Displaying the number of images and image dimensions
for galaxy_class in galaxy_npys.keys():
  galaxy_npys[galaxy_class] = galaxy_npys[galaxy_class][1:]
  print(galaxy_npys[galaxy_class].shape)

# save the data to corresponding .npy file 
for galaxy_class in galaxy_npys.keys():
  temp = np.save(os.path.join(OUTPUT_DIR, galaxy_class+".npy"), galaxy_npys[galaxy_class])

images = np.zeros(shape = (1, IMAGE_SIDE_SIZE, IMAGE_SIDE_SIZE, 3))
# concatenating all images in images array
for galaxy_class in galaxy_npys.keys():
  temp = np.load(os.path.join(OUTPUT_DIR, galaxy_class+".npy"))
  # temp = np.expand_dims(temp, axis = 0)
  images = np.concatenate((images, temp), axis = 0)

images = images[1:]
print(images.shape)

#Displaying elliptical image below
plt.imshow(galaxy_npys["elliptical"][4])
plt.show()
#Displaying irregular image below
plt.imshow(galaxy_npys["irregular"][0])
plt.show()
