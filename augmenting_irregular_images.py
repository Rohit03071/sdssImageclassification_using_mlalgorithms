# Importing all the required libraries
import os
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imgaug as ia
import imgaug.augmenters as iaa

INPUT_DIRECTORY = "D:/Deep learning/Irregular Galaxies/irregular"

RESIZED_OUTPUT_DIRECTORY = "D:/Deep learning/Irregular Galaxies/irregular_resized"

AUG_OUTPUT_DIRECTORY = "D:/Deep learning/Irregular Galaxies/irregular_aug"

IMAGE_SIDE_LENGTH = 128
NUMBER_IMAGES = 800
GROUP_NUMBER = 11

# Resizing all images in input_dir
filenames = os.listdir(INPUT_DIRECTORY)
for filename in filenames:
  temp = cv2.imread(os.path.join(INPUT_DIRECTORY, filename))
  temp = cv2.resize(temp, (IMAGE_SIDE_LENGTH, IMAGE_SIDE_LENGTH))
  cv2.imwrite(os.path.join(RESIZED_OUTPUT_DIRECTORY, filename), temp)

# Loading a 800 images into memory
images = np.zeros((1, IMAGE_SIDE_LENGTH, IMAGE_SIDE_LENGTH, 3), dtype = np.uint8)
filenames = os.listdir(RESIZED_OUTPUT_DIRECTORY)

original_images = len(filenames)

counter = 0
while(images.shape[0] < NUMBER_IMAGES +1):
  # Choose a random index
  choice = random.randint(0, original_images-1)
  # Image file to read (from random index chosen)
  temp = cv2.imread(os.path.join(RESIZED_OUTPUT_DIRECTORY, filenames[choice]))
  # Expand the dimensions of the image you have read in
  temp = np.expand_dims(temp, axis = 0)
  
  counter +=1
  # Concatenate to image directory
  images = np.concatenate((images, temp), axis = 0)

  if counter % 100 ==0:
    print(str(counter), "images loaded.")
images = images[1:]

print(images.shape)

# Sample 15 images
cols = 9
rows = 5

row_images = []

for i in range(rows):
  indices = np.random.rand(cols)
  indices = (indices*NUMBER_IMAGES).astype(np.int64)  

  row = images[indices[0], ...]
  for j in range(1, cols):
    row = np.hstack((row, images[indices[j]]))
  
  row_images.append(row[:])

image = row_images[0]
for i in range(1, rows):
  image = np.vstack((image, row_images[i]))
# Display 
plt.figure(figsize=(cols*3, rows*3))
plt.imshow(image)

ia.seed(GROUP_NUMBER)
#Using augmenter to augment the image
sequential_augmenter = iaa.Sequential([
                                        iaa.ChannelShuffle(0.35),
                                        iaa.ScaleX((0.9, 1.1)),
                                        iaa.ScaleY((0.9, 1.1)),
                                        iaa.Sometimes(0.5, iaa.OneOf([iaa.Fliplr(), iaa.Flipud()])),
                                        iaa.Sometimes(0.5, iaa.Rot90((1,3))),
                                       ], random_order = True)

augmented_images = sequential_augmenter.augment_images(images)

# Sample 15 images
cols = 5
rows = 5

row_images = []

for i in range(rows):
  indices = np.random.rand(cols)
  indices = (indices*NUMBER_IMAGES).astype(np.int64)  

  row = augmented_images[indices[0], ...]
  for j in range(1, cols):
    row = np.hstack((row, augmented_images[indices[j]]))
  
  row_images.append(row[:])

image = row_images[0]
for i in range(1, rows):
  image = np.vstack((image, row_images[i]))

plt.figure(figsize=(cols*3, rows*3))
plt.imshow(image)

#writing the images on the prescribed file path
for i in range(NUMBER_IMAGES):
  fname = "irregular_" + str(i) + ".jpg"
  cv2.imwrite(os.path.join(AUG_OUTPUT_DIRECTORY, fname), augmented_images[i])

  if i % 100 == 0:
    print(str(i), "images written to disk")
