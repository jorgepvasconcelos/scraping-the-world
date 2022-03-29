from selenium import webdriver

from scraping_the_world.scrapers.webdriver_manager.webdriver_toolkit import WebDriverToolKit
from env import ENV


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')

    if ENV['ENV'] == 'DEV':
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
        # driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Remote(command_executor='http://container_selenium:4444/wd/hub',
                                  options=options)  # rodar com docker

    driver.maximize_window()

    wdtk = WebDriverToolKit(driver)

    return driver, wdtk
