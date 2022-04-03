import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError, PageNotFound404Error


class ScrapingAmericanas:
    def __init__(self, url):
        self.__url = url
        self.__site_data = {
            'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None, 'error': False}

    def consult(self):
        scraping_type = int(get_config('scraping_americanas'))
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
            add_log(log_text=f'[scraping_americanas] Traceback: {error}', log_type='ERROR')
            self.__site_data['error'] = error
        finally:
            if webdriver_manager:
                webdriver_manager.driver_quit()

            return self.__site_data

    def __scraping_requests(self):
        session = HTMLSession()
        response = session.get(self.__url).text
        parsel_selector = Selector(text=response)

        selector = '.product-title__Title-sc-1hlrxcw-0::text'
        self.__site_data['titulo'] = parsel_selector.css(selector).get()

        selector = 'div[class="main-image__Container-sc-1i1hq2n-1 iCNHlx"]>div>picture>img::attr(src)'
        self.__site_data['imagem'] = parsel_selector.css(selector).get()

        selector = '.priceSales::text'
        self.__site_data['preco'] = parsel_selector.css(selector).get()

        selector = '.product-description__Description-sc-ytj6zc-1::text'
        descricao = parsel_selector.css(selector).get()
        self.__site_data['descricao'] = descricao if descricao else 'No Description'

        selector = 'head>[property="al:web:url"]::attr(content)'
        self.__site_data['url'] = parsel_selector.css(selector).get()

        return self.__site_data

    def __scraping_selenium(self):
        driver, wdtk = WebdriverManager().get_driver()
        driver.get(self.__url)

        selector = '.product-title__Title-sc-1hlrxcw-0'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = 'div[class="main-image__Container-sc-1i1hq2n-1 iCNHlx"]>div>picture>img'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
        else:
            raise SiteWhithoutDataError()

        selector = '.priceSales'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '.product-description__Description-sc-ytj6zc-1'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            descricao = driver.find_element(By.CSS_SELECTOR, selector).text
            self.__site_data['descricao'] = descricao if descricao else 'No Description'
        else:
            self.__site_data['descricao'] = 'No Description'

        self.__site_data['url'] = driver.current_url

        return self.__site_data


if __name__ == '__main__':
    ...
    scraping_result = ScrapingAmericanas('https://www.americanas.com.br/produto/3068486001').consult()  # no description
    # scraping_result = scraping_americanas('https://www.americanas.com.br/produto/2896992161')  # with description
    print(scraping_result)
