import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError

__site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}


def clean___site_data():
    global __site_data
    __site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}


def scraping_submarino(url):
    clean___site_data()
    scraping_type = int(get_config('scraping_submarino'))
    webdriver_manager = None

    try:
        if scraping_type == 0:
            webdriver_manager = WebdriverManager()
            webdriver_manager.create_driver()
            result = scraping_selenium(url=url)
            webdriver_manager.driver_quit()
            return result
        elif scraping_type == 1:
            return scraping_requests(url=url)
    except:
        if webdriver_manager:
            webdriver_manager.driver_quit()
        add_log(log_text=f'[scraping_submarino] Traceback: {traceback.format_exc()}', log_type='ERROR')
        return __site_data


def scraping_requests(url):
    session = HTMLSession()
    response = session.get(url).text
    parsel_selector = Selector(text=response)

    selector = '.src__Title-sc-1xq3hsd-0::text'
    __site_data['titulo'] = parsel_selector.css(selector).get()

    selector = '.image__WrapperImages-sc-oakrdw-1>div>picture>img::attr(src)'
    __site_data['imagem'] = parsel_selector.css(selector).get()

    selector = '[class="src__BestPrice-sc-1jnodg3-5 ykHPU priceSales"]::text'
    __site_data['preco'] = parsel_selector.css(selector).get()

    selector = '[class="product-description__Description-sc-ytj6zc-1 ecJlZp"]::text'
    descricao = parsel_selector.css(selector).get()
    __site_data['descricao'] = descricao if descricao else 'No Description'

    selector = 'head>[property="al:web:url"]::attr(content)'
    __site_data['url'] = parsel_selector.css(selector).get()

    return __site_data


def scraping_selenium(url):
    driver, wdtk = WebdriverManager().get_driver()
    driver.get(url)

    selector = '.src__Title-sc-1xq3hsd-0'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = '.image__WrapperImages-sc-oakrdw-1>div>picture>img'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
    else:
        raise SiteWhithoutDataError()

    selector = '[class="src__BestPrice-sc-1jnodg3-5 ykHPU priceSales"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = '[class="product-description__Description-sc-ytj6zc-1 ecJlZp"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        descricao = driver.find_element(By.CSS_SELECTOR, selector).text
        __site_data['descricao'] = descricao if descricao else 'No Description'
    else:
        __site_data['descricao'] = 'No Description'

    __site_data['url'] = driver.current_url

    return __site_data


if __name__ == '__main__':
    ...
    scraping_result = scraping_submarino('https://www.submarino.com.br/produto/105016640')  # no description
    # scraping_result = scraping_submarino('https://www.submarino.com.br/produto/1611318018')  # with description
    print(scraping_result)
