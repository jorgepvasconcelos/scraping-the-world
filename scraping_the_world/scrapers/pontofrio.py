import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError, PageNotFound404Error


class ScrapingPontofrio:
    def __init__(self, url):
        self.__url = url
        self.__site_data = {
            'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None, 'error': False}

    def consult(self):
        scraping_type = int(get_config('scraping_pontofrio'))
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
            add_log(log_text=f'[scraping_pontofrio] Traceback: {error}', log_type='ERROR')
            self.__site_data['error'] = error
        finally:
            if webdriver_manager:
                webdriver_manager.driver_quit()

            return self.__site_data

    def __scraping_requests(self):
        session = HTMLSession()
        response = session.get(self.__url).text
        parsel_selector = Selector(text=response)

        selector = '[class=" css-k7ata1 eym5xli0"]::text'
        self.__site_data['titulo'] = parsel_selector.css(selector).get()

        selector = '[class="magnify-container"]>div>img::attr(src)'
        self.__site_data['imagem'] = parsel_selector.css(selector).get()

        selector = '[id="product-price"]::text'
        self.__site_data['preco'] = parsel_selector.css(selector).get()

        # selector = '.product-description__Description-sc-ytj6zc-1::text'
        # descricao = parsel_selector.css(selector).get()
        self.__site_data['descricao'] = 'No Description'

        selector = 'head>[rel="canonical"]::attr(href)'
        self.__site_data['url'] = parsel_selector.css(selector).get()

        return self.__site_data

    def __scraping_selenium(self):
        driver, wdtk = WebdriverManager().get_driver()
        driver.get(self.__url)

        if 'O nosso pinguim não encontrou o que você procurou' in driver.page_source:
            raise PageNotFound404Error()

        selector = '[class=" css-k7ata1 eym5xli0"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '[class="magnify-container"]>div>img'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
        else:
            raise SiteWhithoutDataError()

        selector = '[id="product-price"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        self.__site_data['descricao'] = 'No Description'

        self.__site_data['url'] = driver.current_url

        return self.__site_data


if __name__ == '__main__':
    ...
    scraping_result = ScrapingPontofrio(
        'https://www.pontofrio.com.br/rack-136-madetec-lisboa-para-tv-ate-50/p/11996540').consult()
    # scraping_result = scraping_pontofrio('https://www.pontofrio.com.br/refrigerador-electrolux-duplex-dc35a-260l-branco/p/1743666')
    print(scraping_result)
