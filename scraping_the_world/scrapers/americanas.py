import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError

__site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}


def scraping_americanas(url):
    scraping_type = 0

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
        add_log(log_text=f'[scraping_americanas] Traceback: {traceback.format_exc()}', log_type='ERROR')
        return __site_data


def scraping_requests(url):
    session = HTMLSession()
    response = session.get(url).text
    parsel_selector = Selector(text=response)

    selector = '.product-title__Title-sc-1hlrxcw-0::text'
    __site_data['titulo'] = parsel_selector.css(selector).get()

    selector = 'div[class="main-image__Container-sc-1i1hq2n-1 iCNHlx"]>div>picture>img::attr(src)'
    __site_data['imagem'] = parsel_selector.css(selector).get()

    selector = '.priceSales::text'
    __site_data['preco'] = parsel_selector.css(selector).get()

    selector = '.product-description__Description-sc-ytj6zc-1::text'
    descricao = parsel_selector.css(selector).get()
    __site_data['descricao'] = descricao if descricao else 'No Description'

    selector = 'head>[property="al:web:url"]::attr(content)'
    __site_data['url'] = parsel_selector.css(selector).get()

    return __site_data


def scraping_selenium(url):
    # webdriver_manager = WebdriverManager().get_driver()
    # webdriver_manager.get_driver()
    driver, wdtk = WebdriverManager().get_driver()
    driver.get(url)

    selector = '.product-title__Title-sc-1hlrxcw-0'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = 'div[class="main-image__Container-sc-1i1hq2n-1 iCNHlx"]>div>picture>img'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
    else:
        raise SiteWhithoutDataError()

    selector = '.priceSales'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = '.product-description__Description-sc-ytj6zc-1'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        descricao = driver.find_element(By.CSS_SELECTOR, selector).text
        __site_data['descricao'] = descricao if descricao else 'No Description'
    else:
        __site_data['descricao'] = 'No Description'

    __site_data['url'] = driver.current_url

    return __site_data


if __name__ == '__main__':
    ...
    scraping_result = scraping_americanas('https://www.americanas.com.br/produto/3068486001')  # no description
    # scraping_result = scraping_americanas('https://www.americanas.com.br/produto/2896992161')  # with description
    print(scraping_result)
