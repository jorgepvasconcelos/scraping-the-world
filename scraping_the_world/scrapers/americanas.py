from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

from webdriver_toolkit import WebDriverToolKit


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')

    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    # driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    wdtk = WebDriverToolKit(driver)

    return driver, wdtk


def scraping_americanas(url):
    site_data = {'titulo': None, 'imagem': None, 'preco': None, 'url': None}

    driver, wdtk = get_driver()
    driver.get(url)

    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, '.priceSales')):
        site_data['preco'] = driver.find_element(By.CSS_SELECTOR, '.priceSales').text

    driver.quit()

    return site_data


if __name__ == '__main__':
    scraping_result = scraping_americanas('https://www.americanas.com.br/produto/3068486001')
    print(scraping_result)
