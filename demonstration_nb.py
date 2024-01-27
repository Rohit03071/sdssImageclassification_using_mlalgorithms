
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
import cv2
import pandas as pd


df = pd.DataFrame(columns=['Actual', 'Predicted'])

# Import PCA datastet
LABELS_PATH = "D:/Deep learning/galaxy-image-classification-main/pca_dataset/labels.npy"
IMG_PATH = "D:/Deep learning/galaxy-image-classification-main/pca_dataset/images.npy"

# Y as it has labels for particular image
labels = np.load(LABELS_PATH) 
images = np.load(IMG_PATH) 

IMAGE_SIDE_SIZE = 128

CLASS_NAMES = ["elliptical", "spiral", "irregular", "invalid"]

X = np.load(IMG_PATH)
y = np.load(LABELS_PATH)

MLP_PATH = os.path.join("D:/Deep learning/galaxy-image-classification-main/CNNmodel", "mlp_model.h5")
CNN_PATH = os.path.join("D:/Deep learning/galaxy-image-classification-main/CNNmodel", "cnn_model.h5")
from keras.models import load_model

cnn_model = load_model(CNN_PATH)
mlp_model = load_model(MLP_PATH)
cnn_predictions = cnn_model.predict(X)
cnn_predictions = np.argmax(cnn_predictions, axis = -1)


mlp_predictions = mlp_model.predict(X)
mlp_predictions = np.argmax(mlp_predictions, axis = -1)


import random
# sample images
cols = 3
rows = 3
NO_INDICES = X.shape[0]
plt.figure(figsize=(cols*5, rows*5.7))
for i in range(rows):
  for j in range(cols):
    
    ax = plt.subplot(rows, cols, i*cols + j+1)
    indx = random.randint(0, X.shape[0]-1)

    cnn_pred = cnn_predictions[indx]
    mlp_pred = mlp_predictions[indx]

    title_string = "GT:" + str(CLASS_NAMES[y[indx]])
    title_string += "\nCNN:" + str(CLASS_NAMES[cnn_pred] + " | MLP:" + str(CLASS_NAMES[mlp_pred]))

    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.set_title(title_string, fontdict={"fontsize": 18})
    ax.imshow(cv2.cvtColor((images[indx]*255).astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.show()
