# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YIhQvVVSeGGwopoT7ol6pVBtNVjK3ohw
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import cv2 as cv
import io

train_path = "/content/datasets"

train_datagen = ImageDataGenerator(
    rescale = 1./255, 
    shear_range = 0.2, 
    zoom_range = 0.2,
    validation_split = 0.25
)
train_set = train_datagen.flow_from_directory(
    train_path, 
    target_size = (45, 45), 
    color_mode = 'grayscale',
    batch_size = 32,
    class_mode = 'categorical',
    classes = ['+','1','2','3','4','5','6','7','8','9','=','X','^','y'],
    shuffle = True,
    subset='training',
    seed = 123
)

test_set = train_datagen.flow_from_directory(
    train_path, 
    target_size = (45, 45), 
    color_mode = 'grayscale',
    batch_size = 32,
    class_mode = 'categorical',
    classes =  ['+','1','2','3','4','5','6','7','8','9','=','X','^','y'],
    shuffle = True,
    subset='validation',
    seed = 123
)

model = tf.keras.models.Sequential()

# First Convolutional Block
model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=(5,5), padding='same', activation='relu', input_shape=(45, 45, 1)))
model.add(tf.keras.layers.MaxPool2D(strides=2))

# Second Convolutional Block
model.add(tf.keras.layers.Conv2D(filters=48, kernel_size=(5,5), padding='valid', activation='relu'))
model.add(tf.keras.layers.MaxPool2D(strides=2))

# Classifier Head
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(84, activation='relu'))
model.add(tf.keras.layers.Dense(14, activation='softmax'))

adam = tf.keras.optimizers.Adam(learning_rate = 5e-4)
model.compile(optimizer = adam, loss = 'categorical_crossentropy', metrics = ['accuracy'])

model.fit(train_set, validation_data = test_set, batch_size=128, epochs = 30)

val_loss, val_accuracy = model.evaluate(test_set)
print(val_loss,val_accuracy)

save_path= " "

model.save(os.path.join(save_path,"model.h5"))

from tensorflow.keras.models import load_model

model2 = load_model(os.path.join(save_path,'model.h5'))

#!unrar x /content/drive/MyDrive/yotadhukkafinal.rar