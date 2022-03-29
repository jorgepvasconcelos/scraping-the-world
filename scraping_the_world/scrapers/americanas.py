from selenium.webdriver.common.by import By

from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import get_driver


def scraping_americanas(url):
    site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}

    driver, wdtk = get_driver()
    driver.get(url)

    selector = '.product-title__Title-sc-1hlrxcw-0'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text

    selector = 'div[class="main-image__Container-sc-1i1hq2n-1 iCNHlx"]>div>picture>img'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')

    selector = '.priceSales'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text

    selector = '.product-description__Description-sc-ytj6zc-1'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['descricao'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        site_data['descricao'] = 'No Description'

    site_data['url'] = driver.current_url

    driver.quit()

    return site_data


if __name__ == '__main__':
    ...
    # scraping_result = scraping_americanas('https://www.americanas.com.br/produto/3068486001') # no description
    # scraping_result = scraping_americanas('https://www.americanas.com.br/produto/2896992161')  # with description
    # print(scraping_result)
