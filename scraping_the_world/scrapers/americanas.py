from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')

    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    driver.maximize_window()

    return driver


def scraping_americanas(url):
    print("Test Execution Started")

    driver = get_driver()
    driver.get(url)
    sleep(10)
    var = driver.find_element(By.CSS_SELECTOR, '.priceSales').text

    driver.close()
    driver.quit()
    return var


if __name__ == '__main__':
    scraping_result = scraping_americanas('https://www.americanas.com.br/produto/3068486001')
    print(scraping_result)
