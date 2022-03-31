import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError

__site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}


def scraping_pontofrio(url):
    scraping_type = int(get_config('scraping_pontofrio'))
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
        add_log(log_text=f'[scraping_pontofrio] Traceback: {traceback.format_exc()}', log_type='ERROR')
        return __site_data


def scraping_requests(url):
    session = HTMLSession()
    response = session.get(url).text
    parsel_selector = Selector(text=response)

    selector = '[class=" css-k7ata1 eym5xli0"]::text'
    __site_data['titulo'] = parsel_selector.css(selector).get()

    selector = '[class="magnify-container"]>div>img::attr(src)'
    __site_data['imagem'] = parsel_selector.css(selector).get()

    selector = '[id="product-price"]::text'
    __site_data['preco'] = parsel_selector.css(selector).get()

    # selector = '.product-description__Description-sc-ytj6zc-1::text'
    # descricao = parsel_selector.css(selector).get()
    __site_data['descricao'] = 'No Description'

    selector = 'head>[rel="canonical"]::attr(href)'
    __site_data['url'] = parsel_selector.css(selector).get()

    return __site_data


def scraping_selenium(url):
    driver, wdtk = WebdriverManager().get_driver()
    driver.get(url)

    selector = '[class=" css-k7ata1 eym5xli0"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = '[class="magnify-container"]>div>img'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
    else:
        raise SiteWhithoutDataError()

    selector = '[id="product-price"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    __site_data['descricao'] = 'No Description'

    __site_data['url'] = driver.current_url

    return __site_data


if __name__ == '__main__':
    ...
    # scraping_result = scraping_pontofrio('https://www.pontofrio.com.br/rack-136-madetec-lisboa-para-tv-ate-50/p/11996540')
    # scraping_result = scraping_pontofrio('https://www.pontofrio.com.br/refrigerador-electrolux-duplex-dc35a-260l-branco/p/1743666')
    # print(scraping_result)
