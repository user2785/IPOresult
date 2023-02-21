import CaptchaCracker as cc
import glob
import warnings
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

imgdir = 'data/test_numbers_only'
filelist = [f for f in glob.glob(imgdir + "**/*.png", recursive=True)]

img_width = 150
img_height = 40
max_length = 5
characters = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

# Model weight file path
weights_path = "model.h5"
AM = cc.ApplyModel(weights_path, img_width, img_height, max_length, characters)

# Predicted value
x = 0
for files in filelist:
    prediction = AM.predict(files)
    if prediction + ".png" == os.path.basename(files):
        x = x + 1

print("accuracy = " + str(x/len(filelist)*100) + " %")

