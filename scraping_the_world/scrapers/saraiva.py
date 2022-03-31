import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError

__site_data = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}


def scraping_saraiva(url):
    scraping_type = int(get_config('scraping_saraiva'))
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
        add_log(log_text=f'[scraping_saraiva] Traceback: {traceback.format_exc()}', log_type='ERROR')
        return __site_data


def scraping_requests(url):
    session = HTMLSession()
    response = session.get(url).text
    parsel_selector = Selector(text=response)

    selector = '[class="page-title-box"]>h1::text'
    __site_data['titulo'] = parsel_selector.css(selector).get()

    selector = '[class="tab-pane active show"]>[class="img-fluid mx-auto d-block rounded imgGaleryResponsive"]::attr(src)'
    __site_data['imagem'] = parsel_selector.css(selector).get()

    selector = '[class="mb-0 price-destaque"]::text'
    __site_data['preco'] = parsel_selector.css(selector).get()

    selector = '[id="descricao"]::text'
    descricao = parsel_selector.css(selector).get()
    __site_data['descricao'] = descricao if descricao else 'No Description'

    selector = '[itemprop="url"]::attr(content)'
    __site_data['url'] = parsel_selector.css(selector).get()

    return __site_data


def scraping_selenium(url):
    driver, wdtk = WebdriverManager().get_driver()
    driver.get(url)

    page_text = 'Pagina não encontrada'
    if wdtk.text_is_present(wait_time=2, locator=(By.TAG_NAME, 'html'), text=page_text):
        return __site_data

    selector = '[class="page-title-box"]>h1'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = '[class="tab-pane active show"]>[class="img-fluid mx-auto d-block rounded imgGaleryResponsive"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
    else:
        raise SiteWhithoutDataError()

    selector = '[class="mb-0 price-destaque"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        __site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
    else:
        raise SiteWhithoutDataError()

    selector = '[id="descricao"]'
    if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
        descricao = driver.find_element(By.CSS_SELECTOR, selector).text
        __site_data['descricao'] = descricao if descricao else 'No Description'
    else:
        __site_data['descricao'] = 'No Description'

    __site_data['url'] = driver.current_url

    return __site_data


if __name__ == '__main__':
    ...
    # with description
    # scraping_result = scraping_saraiva('https://www.saraiva.com.br/box-o-essencial-da-psicologia-3-volumes-10081856/p')
    # without description
    # scraping_result = scraping_saraiva('https://www.saraiva.com.br/sobre-a-brevidade-da-vida-edicao-especial-com-prefacio-de-lucia-helena-galvao-maya--capa-es-20086735/p')
    # print(scraping_result)
