from selenium.webdriver.common.by import By

from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import get_driver


def scraping_submarino(url):
    site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}

    driver, wdtk = get_driver()
    driver.get(url)

    selector = '.src__Title-sc-1xq3hsd-0'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text

    selector = '.image__WrapperImages-sc-oakrdw-1>div>picture>img'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')

    selector = '[class="src__BestPrice-sc-1jnodg3-5 ykHPU priceSales"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text

    selector = '[class="product-description__Description-sc-ytj6zc-1 ecJlZp"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        site_data['descricao'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        site_data['descricao'] = 'No Description'

    site_data['url'] = driver.current_url

    driver.quit()

    return site_data


if __name__ == '__main__':
    ...
    scraping_result = scraping_submarino('https://www.submarino.com.br/produto/105016640')  # no description
    # scraping_result = scraping_submarino('https://www.americanas.com.br/produto/2896992161')  # with description
    print(scraping_result)
