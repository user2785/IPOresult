
import os
from CaptchaCracker import ApplyModel


# Function to get captcha from trained model
def auto_captcha_solver(img_path):
    img_width = 150
    img_height = 40
    max_length = 5
    characters = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    model_path = "Captcha_solve/model.h5"
    AM = ApplyModel(model_path, img_width, img_height, max_length, characters)
    prediction = AM.predict(img_path)
    return prediction

# Function to Enter Captcha and to Check for error
def get_captcha():
    while True:
        captcha_solved = auto_captcha_solver('captcha_element.png')  # auto decode captcha_element from tensorflow model
        os.remove('captcha_element.png')    
        if len(captcha_solved) != 5:
            continue
        return captcha_solved