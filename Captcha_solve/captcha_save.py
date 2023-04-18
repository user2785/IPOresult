import re
import urllib.request
import io
import os
import base64
import CaptchaCracker as cc
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec



def auto_captcha_solver(img_path):
    img_width = 150
    img_height = 40
    max_length = 5
    characters = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    model_path = "model.h5"
    AM = cc.ApplyModel(model_path, img_width, img_height, max_length, characters)
    imgdir = img_path
    pred = AM.predict(imgdir)
    return pred


# Function to Check Connection
def connection_check(host):
    try:
        urllib.request.urlopen(host)
    except:
        print("\nError: Connection Failed...")
        exit()


# Function to wait for site to load
def wait():
    try:
        WebDriverWait(browser, 10).until(
            ec.presence_of_element_located(
                (
                    By.CSS_SELECTOR, '#companyShare > option:nth-child(4)')
            )
        )
    finally:
        print("")


number_of_img = int(input("no of images to save: "))
url = "https://iporesult.cdsc.com.np"
browser = webdriver.Firefox()
browser.get(url)

connection_check(url)  # Call connection_check function
wait()  # Call wait function

company = browser.find_element(By.ID, "companyShare")
sel = Select(company)
sel.select_by_index(1)
text = browser.find_element(By.ID, "boid")
text.send_keys('1300000000000000')

i = 0
while True:
    captcha = browser.find_element(By.ID, "userCaptcha")
    captcha.click()
    image = browser.find_element(By.XPATH, '//img[@alt="captcha"]').get_attribute("src")
    recompile = re.compile(r'data:image/png;base64,.*', re.DOTALL)
    base64data = recompile.search(image)
    data = base64data.group()[22:]
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(data, "utf-8"))))
    img.save('captcha.png')
    pred = auto_captcha_solver('captcha.png')
    captcha.send_keys(pred)
    while True:
        if len(captcha.get_attribute("value")) == 5:
            break

    submit = browser.find_element(By.XPATH,
                                  "/html/body/app-root/app-allotment-result/div/div/div/div/form/button")
    submit.click()
    result = browser.find_element(By.XPATH, "/html/body/app-root/app-allotment-result/div/div/div/div/form/p[2]").text
    reload = browser.find_element(By.XPATH,
                                  '/html/body/app-root/app-allotment-result/div/div/div/div/form/div[2]/div[2]/div/div[2]/button[2]')
    if result == "Invalid Captcha Provided. Please try again":
        captcha.clear()
        reload.click()
        print("EEROR")
        continue
    os.remove('captcha.png')
    img.save(pred + ".png")
    os.replace(pred + ".png", "data/" + pred + ".png")
    captcha.clear()
    i = i + 1
    if  i >= number_of_img:
        break
browser.quit()
print("/n Note: move the image files to train and test files in 80:20 ratio")