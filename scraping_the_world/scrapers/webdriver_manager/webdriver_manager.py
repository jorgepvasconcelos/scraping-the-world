import os

from selenium import webdriver

from scraping_the_world.scrapers.webdriver_manager.webdriver_toolkit import WebDriverToolKit
from env import ENV

WEBDRIVERS_PATH = os.path.dirname(os.path.realpath(__file__))


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--enable-automation')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36')

    # options.add_argument('--headless')

    if ENV['ENV'] == 'DEV':
        if int(ENV['SELENIUM_REMOTE']) == 1:
            driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
        else:
            webdriver_path = f'{WEBDRIVERS_PATH}\\chromedriver'
            driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    else:
        driver = webdriver.Remote(command_executor='http://container_selenium:4444/wd/hub', options=options)

    driver.maximize_window()

    wdtk = WebDriverToolKit(driver)

    return driver, wdtk
