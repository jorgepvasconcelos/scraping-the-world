import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError, PageNotFound404Error


class ScrapingZattini:
    def __init__(self, url):
        self.__url = url
        self.__site_data = {
            'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None, 'error': False}

    def consult(self):
        scraping_type = int(get_config('scraping_zattini'))
        webdriver_manager = None

        try:
            if scraping_type == 0:
                webdriver_manager = WebdriverManager()
                webdriver_manager.create_driver()
                self.__scraping_selenium()
            elif scraping_type == 1:
                self.__scraping_requests()
        except PageNotFound404Error as error:
            self.__site_data['error'] = error
        except SiteWhithoutDataError as error:
            self.__site_data['error'] = error
        except Exception as error:
            add_log(log_text=f'[scraping_zattini] Traceback: {error}', log_type='ERROR')
            self.__site_data['error'] = error
        finally:
            if webdriver_manager:
                webdriver_manager.driver_quit()

            return self.__site_data

    def __scraping_requests(self):
        session = HTMLSession()
        response = session.get(self.__url).text
        parsel_selector = Selector(text=response)

        page_text = 'Ops! A página que você procura está temporariamente indisponível ou foi removida.'
        if page_text in response:
            raise PageNotFound404Error()

        selector = 'h1[data-productname]::text'
        self.__site_data['titulo'] = parsel_selector.css(selector).get()

        selector = '[class="photo-figure"]>.zoom::attr(src)'
        self.__site_data['imagem'] = parsel_selector.css(selector).get()

        selector = '[class="default-price"]>span>strong::text'
        self.__site_data['preco'] = parsel_selector.css(selector).get()

        selector = '[itemprop="description"]::text'
        descricao = parsel_selector.css(selector).get()
        self.__site_data['descricao'] = descricao if descricao else 'No Description'

        selector = '[rel="canonical"]::attr(href)'
        self.__site_data['url'] = parsel_selector.css(selector).get()

        return self.__site_data

    def __scraping_selenium(self):
        driver, wdtk = WebdriverManager().get_driver()
        driver.get(self.__url)

        page_text = 'Ops! A página que você procura está temporariamente indisponível ou foi removida.'
        if wdtk.text_is_present(wait_time=2, locator=(By.TAG_NAME, 'html'), text=page_text):
            raise PageNotFound404Error()

        selector = 'h1[data-productname]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '[class="photo-figure"]>.zoom'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
        else:
            raise SiteWhithoutDataError()

        selector = '[class="default-price"]>span>strong'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '[itemprop = "description"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            descricao = driver.find_element(By.CSS_SELECTOR, selector).text
            self.__site_data['descricao'] = descricao if descricao else 'No Description'
        else:
            self.__site_data['descricao'] = 'No Description'

        self.__site_data['url'] = driver.current_url

        return self.__site_data


if __name__ == '__main__':
    ...
    # with description
    url = 'https://www.zattini.com.br/tenis-reserva-vela-masculino-preto+branco-B67-5119-026'
    # 404Page
    # url = 'https://www.zattini.com.br/tenis-reserva-vela-masculino-preto+br55anco-B67-511966666-026'
    scraping_result = ScrapingZattini(url).consult()
    print(scraping_result)
