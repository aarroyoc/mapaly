import os

from selenium import webdriver


def get_selenium_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1350,720")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = os.environ.get(
        "SELENIUM_CHROME", "/usr/bin/chromium"
    )
    return webdriver.Chrome(chrome_options=chrome_options)
