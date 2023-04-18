import glob
import CaptchaCracker
import tensorflow as tf
import warnings
import numpy as np
import os
import logging


warnings.simplefilter(action='ignore', category=FutureWarning)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel(logging.ERROR)
# Training image data path
train_img_path_list = glob.glob("data/train_numbers_only/*.png")

# Training image data size
img_width = 150
img_height = 40

# Creating an instance that creates a model
CM = CaptchaCracker.CreateModel(train_img_path_list, img_width, img_height)

# Performing model training
model = CM.train_model(epochs=100)

# Saving the weights learned by the model to a file
model.save_weights("model.h5")