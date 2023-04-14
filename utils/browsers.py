import re
import io
import base64
from time import sleep
from PIL import Image
from colorama import Fore, Style
from utils.captcha_crack import get_captcha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import utils.func



# Function to open browser(Chrome, Edge, Firefox)
def browser_open(url):
    global browser
    try:
        print('..chrome..',end='')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        print("Chrome driver created successfully")
    except:
        try:
            print('..edge..',end='')
            chrome_options = webdriver.EdgeOptions()
            chrome_options.add_argument('--headless')
            browser = webdriver.Edge(options=chrome_options)
            print("Edge driver created successfully")
        except:
            try:
                print('..firefox..',end='')
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.headless = True
                browser = webdriver.Firefox(options=firefox_options)
                print("Firefox driver created successfully")
            except:
                print("\nError while opening browser.......")
                print("....run webdriver.py first")
                close_all()

    browser.get(url)   # Wait until webpage is loaded
    WebDriverWait(browser, 20).until(
        ec.presence_of_element_located((
                By.CSS_SELECTOR, '#companyShare > option:nth-child(4)')
                )
        )


# Function to list company from the webpage
def list_company():
    print("\n\t" + Fore.BLUE + Style.BRIGHT + browser.title + "\n")
    company = browser.find_element(By.ID, "companyShare")
    option = browser.find_elements(By.CSS_SELECTOR, "#companyShare > option", )
    for index, text in enumerate(option):
        print(f'{index} > {text.text}')
    return Select(company), option


# Function to check for the Result
def check(client_boid, client_name, iteration):
    text = browser.find_element(By.ID, "boid")
    text.clear()
    text.send_keys(client_boid)
    try:
        result = browser.find_element(By.XPATH, "/html/body/app-root/app-allotment-result/div/div/div/div/form/div[3]/p").text
    finally:
        if 'Invalid' in result:
            print(client_name + " : " + client_boid + " is incorrect. Correct before continue")
            close_all()  
    if iteration == 1:
        #thread.join()
        iteration = 0
    while True:
        save_img()  # Function to save captcha_element to file
        captcha_value = get_captcha()  # Call get_captcha function
        utils.func.clear_line(1)
        captcha_element = browser.find_element(By.ID, "userCaptcha")
        captcha_element.send_keys(captcha_value)

        browser.find_element(By.XPATH,
                "/html/body/app-root/app-allotment-result/div/div/div/div/form/button").click()
        sleep(0.3)
        try:       
            result = browser.find_element(By.XPATH,
                        "/html/body/app-root/app-allotment-result/div/div/div/div/form/p[1]").text
            if result == '':
                result = browser.find_element(By.XPATH,
                        "/html/body/app-root/app-allotment-result/div/div/div/div/form/p[2]").text
        finally:          
            if "Connection" in result:
                print("Error: " + result)
                close_all()  # Call close_all function
            if "Captcha" in result:
                continue
            if result == '':
                close_all() 
            else:
                return result
    

# Function to save captcha_element temorarily
def save_img():
    image = browser.find_element(By.XPATH,
                        '/html/body/app-root/app-allotment-result/div/div/div/div/form/div[2]/div[2]/div/div[1]/img').get_attribute("src")
    recompile = re.compile(r'data:image/png;base64,.*', re.DOTALL)
    base64data = recompile.search(image)
    data1 = base64data.group()[22:]
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(data1, "utf-8"))))
    img.save("captcha_element" + ".png")


# Function to close all running instances
def close_all():
    try:
        utils.func.close_wb()
        browser.quit()
    finally:
        exit()