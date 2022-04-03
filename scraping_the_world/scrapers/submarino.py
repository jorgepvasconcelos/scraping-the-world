import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError, PageNotFound404Error


class ScrapingSubmarino:
    def __init__(self, url):
        self.__url = url
        self.__site_data = {
            'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None, 'error': False}

    def consult(self):
        scraping_type = int(get_config('scraping_submarino'))
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
            add_log(log_text=f'[scraping_submarino] Traceback: {error}', log_type='ERROR')
            self.__site_data['error'] = error
        finally:
            if webdriver_manager:
                webdriver_manager.driver_quit()

            return self.__site_data

    def __scraping_requests(self):
        session = HTMLSession()
        response = session.get(self.__url).text
        parsel_selector = Selector(text=response)

        selector = '.src__Title-sc-1xq3hsd-0::text'
        self.__site_data['titulo'] = parsel_selector.css(selector).get()

        selector = '.image__WrapperImages-sc-oakrdw-1>div>picture>img::attr(src)'
        self.__site_data['imagem'] = parsel_selector.css(selector).get()

        selector = '[class="src__BestPrice-sc-1jnodg3-5 ykHPU priceSales"]::text'
        self.__site_data['preco'] = parsel_selector.css(selector).get()

        selector = '[class="product-description__Description-sc-ytj6zc-1 ecJlZp"]::text'
        descricao = parsel_selector.css(selector).get()
        self.__site_data['descricao'] = descricao if descricao else 'No Description'

        selector = 'head>[property="al:web:url"]::attr(content)'
        self.__site_data['url'] = parsel_selector.css(selector).get()

        return self.__site_data

    def __scraping_selenium(self):
        driver, wdtk = WebdriverManager().get_driver()
        driver.get(self.__url)

        selector = '.src__Title-sc-1xq3hsd-0'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '.image__WrapperImages-sc-oakrdw-1>div>picture>img'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
        else:
            raise SiteWhithoutDataError()

        selector = '[class="src__BestPrice-sc-1jnodg3-5 ykHPU priceSales"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '[class="product-description__Description-sc-ytj6zc-1 ecJlZp"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            descricao = driver.find_element(By.CSS_SELECTOR, selector).text
            self.__site_data['descricao'] = descricao if descricao else 'No Description'
        else:
            self.__site_data['descricao'] = 'No Description'

        self.__site_data['url'] = driver.current_url
    
        return self.__site_data


if __name__ == '__main__':
    ...
    url = 'https://www.submarino.com.br/produto/105016640'
    scraping_result = ScrapingSubmarino(url).consult()  # no description
    # scraping_result = scraping_submarino('https://www.submarino.com.br/produto/1611318018')  # with description
    print(scraping_result)
