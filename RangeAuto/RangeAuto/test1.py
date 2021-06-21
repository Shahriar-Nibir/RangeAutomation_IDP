import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image

pb_model_dir = "M:\my_mobilenet_model\saved_model"
h5_model = "M:\my_mobilenet_model\saved_model\mymodel.h5"

# Loading the Tensorflow Saved Model (PB)
model = tf.keras.models.load_model(pb_model_dir)

# Saving the Model in H5 Format
tf.keras.models.save_model(model, h5_model)

# Loading the H5 Saved Model
loaded_model_from_h5 = tf.keras.models.load_model(h5_model)
