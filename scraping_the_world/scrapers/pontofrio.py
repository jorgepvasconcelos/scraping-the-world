from selenium.webdriver.common.by import By

from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import get_driver


def scraping_pontofrio(url):
    site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}

    driver, wdtk = get_driver()
    driver.get(url)

    selector = '[class=" css-k7ata1 eym5xli0"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text

    selector = '[class="magnify-container"]>div>img'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')

    selector = '[id="product-price"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text

    site_data['descricao'] = 'No Description'

    site_data['url'] = driver.current_url

    driver.quit()

    return site_data


if __name__ == '__main__':
    ...
    # scraping_result = scraping_pontofrio('https://www.pontofrio.com.br/rack-136-madetec-lisboa-para-tv-ate-50/p/11996540')
    # scraping_result = scraping_pontofrio('https://www.pontofrio.com.br/refrigerador-electrolux-duplex-dc35a-260l-branco/p/1743666')
    # print(scraping_result)
