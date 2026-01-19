import sys
import io

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Now, import TensorFlow and other libraries
import tensorflow as tf
import pandas as pd
import os

from tensorflow.keras import layers, models # type: ignore

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint # type: ignore
import matplotlib.pyplot as plt
from sklearn.utils import class_weight
import numpy as np

# Your TensorFlow model code goes here
# ---------------------------
# Example: Basic TensorFlow model
# Replace this with your actual model code
print("TensorFlow is working!")

# (Add the rest of your model code as needed)
