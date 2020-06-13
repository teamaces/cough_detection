from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import os
import matplotlib
matplotlib.use('Agg') # No pictures displayed 
import pylab
import librosa
import librosa.display
import numpy as np
import pathlib
   
# audioname = 'C:/Users/Shuvam/Downloads/snipped10.wav'
CATEGORIES = ['Coughing', 'Non-Coughing']
checkpoint = 'model/model.h5'

def wav2melspectogram(audioname):
    y, sr = librosa.load(audioname, mono=True, duration=5)
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
    S = librosa.feature.melspectrogram(y, sr=sr)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    audio_image = f'{audioname[:-3].replace(".", "")}.png'
    pylab.savefig(audio_image, bbox_inches=None, pad_inches=0)
    pylab.close()
    return audio_image

def prepare(filepath):
    IMG_HEIGHT = 480
    IMG_WIDTH = 640
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (IMG_WIDTH, IMG_HEIGHT))
    return new_array.reshape(-1, IMG_HEIGHT, IMG_WIDTH, 3)

def predict_cough_sound(audioname):
    image = wav2melspectogram(audioname)
    model = load_model(checkpoint)
    prediction = model.predict([prepare(image)])
    return CATEGORIES[int(prediction[0][0])]