# -*- coding: utf-8 -*-
"""AMRISHAMAHINDI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aEDOjTJWB3XAoxCZrj9C--1o7nmdPwlB
"""



from google.colab import drive
drive.mount('/content/drive')

"""LOADING DATASET"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

"""SPLITTING DATA """

# Commented out IPython magic to ensure Python compatibility.
# %pip install split-folders[full]

import splitfolders
input_folder = '/content/drive/MyDrive/MaizeData'
splitfolders.ratio(input_folder, output="dataset",
                   seed=42, ratio=(.7, .2, .1),
                   group_prefix=None)

"""BUILDING IMAGE DATA GENERATOR"""

from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions

import keras
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.utils import load_img

"""Exploratory data analysis"""

os.listdir("/content/dataset/train")
os.listdir("/content/dataset/test")
os.listdir("/content/dataset/val")

train_datagen = ImageDataGenerator(zoom_range= 0.5, shear_range= 0.3, horizontal_flip= True, preprocessing_function= preprocess_input) 
val_datagen = ImageDataGenerator(preprocessing_function= preprocess_input)

train = train_datagen.flow_from_directory(directory= "/content/dataset/train", target_size= (256,256), batch_size=32)
val = val_datagen.flow_from_directory(directory= "/content/dataset/val", target_size= (256,256), batch_size=32)

"""

```
# This is formatted as code
```

image preprocessing and feature extraction
"""

t_img , label = train.next()

def plotImage(img_arr, label): 
  for im , l in zip(img_arr , label):
   plt.figure(figsize=(5,5))
   plt.imshow(im)
   plt.show()

plotImage(t_img[:3], label[:3])

"""**BUILDING THE MODEL**"""

from keras.layers import Dense, Flatten
from keras.models import Model
from keras.applications.vgg19 import VGG19
import keras

base_model = VGG19(input_shape=(256,256,3), include_top= False)

for layer in base_model.layers:
  layer.traainable = False

base_model.summary()

x = Flatten()(base_model.output)

x = Dense(units= 4, activation='softmax')(x)


#creating the model
model = Model(base_model.input, x)

from tensorflow.keras.layers import Dense, Dropout, Flatten

# Add new fully connected layers on top of the pre-trained layers
x = base_model.output
x = Flatten()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(4, activation='softmax')(x)

model.summary

"""Compiling the Model."""

model.compile(optimizer= 'adam' , loss= keras.losses.categorical_crossentropy , metrics= ['accuracy'])

"""Early Stopping and Model checkpoint"""

from keras.callbacks import ModelCheckpoint, EarlyStopping
# early stopping
es = EarlyStopping(monitor= 'val_accuracy', min_delta= 0.01, patience= 4,verbose= 1)

# Model Checkpoint
mc = ModelCheckpoint(filepath="best-model.h5", monitor= 'val_accuracy', min_delta= 0.01, patience= 4, verbose= 1 , save_best_only= True)
cb = [es, mc]

from tensorflow.keras.models import Model

model.compile(optimizer= 'adam' , loss= keras.losses.categorical_crossentropy , metrics= ['accuracy'])

History = model.fit_generator(train, steps_per_epoch= 60, epochs= 16, verbose= 1 , callbacks= cb , validation_data= val ,validation_steps= 20)

"""plotting the model"""

h = History.history
h.keys()

plt.plot(h['accuracy'])
plt.plot(h['val_accuracy'] , c = 'red')
plt.title("acc vs v-acc")
plt.show()

plt.plot(h['loss'])
plt.plot(h['val_loss'] , c = "red")
plt.title("loss vs v-loss")
plt.show()

# load best model

from keras.models import load_model

model = load_model("/content/best-model.h5")

acc = model.evaluate_generator(val)[1]

print(f"The accuracy of the model is = {acc*100} %")

ref = dict(zip( list(train.class_indices.values()) , list(train.class_indices.keys()) ) )

ref = dict(zip( list(train.class_indices.values()) , list(train.class_indices.keys()) ) )

train.class_indices

def prediction(path):

  img = load_img(path, target_size= (256,256))

  i = img_to_array(img)

  im = preprocess_input(i)

  img = np.expand_dims(im , axis= 0)

  pred = np.argmax(model.predict(img) )

  print(f" The Image belongs to { ref[pred] }")

path = "/content/dataset/test/Gray_Leaf_Spot/Corn_Gray_Spot (213).jpg"

prediction(path)

!mkdir /content/musu

model.save('/content/musu')

import tensorflow as tf

# Load the SavedModel
model = tf.saved_model.load('/content/musu')

# Convert the SavedModel to a TensorFlow Lite model
converter = tf.lite.TFLiteConverter.from_saved_model('/content/musu')
tflite_model = converter.convert()

# Save the TensorFlow Lite model to a file
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)