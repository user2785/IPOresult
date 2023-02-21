from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import shutil

browser = input("which browser do you want to use:\n1. Chrome\n2. Firefox\n3. Edge\n")


if browser == '1':
    chrome_driver_path = ChromeDriverManager().install()
    shutil.move(chrome_driver_path, './chromedriver.exe')
elif browser == '2':
    firefox_driver_path = GeckoDriverManager().install()
    shutil.move(firefox_driver_path, './geckodriver.exe')
elif browser == '3':
    edge_driver_path = EdgeChromiumDriverManager().install()
    shutil.move(edge_driver_path, './msedgedriver.exe')
else:
    print("Bad input")
