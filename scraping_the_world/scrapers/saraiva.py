import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError, PageNotFound404Error


class ScrapingSaraiva:
    def __init__(self, url):
        self.__url = url
        self.__site_data = {
            'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None, 'error': False}

    def consult(self):
        scraping_type = int(get_config('scraping_saraiva'))
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
            add_log(log_text=f'[scraping_saraiva] Traceback: {error}', log_type='ERROR')
            self.__site_data['error'] = error
        finally:
            if webdriver_manager:
                webdriver_manager.driver_quit()

            return self.__site_data

    def __scraping_requests(self):
        session = HTMLSession()
        response = session.get(self.__url).text
        parsel_selector = Selector(text=response)

        selector = '[class="page-title-box"]>h1::text'
        self.__site_data['titulo'] = parsel_selector.css(selector).get()

        selector = '[class="tab-pane active show"]>[class="img-fluid mx-auto d-block rounded imgGaleryResponsive"]::attr(src)'
        self.__site_data['imagem'] = parsel_selector.css(selector).get()

        selector = '[class="mb-0 price-destaque"]::text'
        self.__site_data['preco'] = parsel_selector.css(selector).get()

        selector = '[id="descricao"]::text'
        descricao = parsel_selector.css(selector).get()
        self.__site_data['descricao'] = descricao if descricao else 'No Description'

        selector = '[itemprop="url"]::attr(content)'
        self.__site_data['url'] = parsel_selector.css(selector).get()

        return self.__site_data

    def __scraping_selenium(self):
        driver, wdtk = WebdriverManager().get_driver()
        driver.get(self.__url)

        page_text = 'Pagina não encontrada'
        if wdtk.text_is_present(wait_time=2, locator=(By.TAG_NAME, 'html'), text=page_text):
            raise PageNotFound404Error()

        selector = '[class="page-title-box"]>h1'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '[class="tab-pane active show"]>[class="img-fluid mx-auto d-block rounded imgGaleryResponsive"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
        else:
            raise SiteWhithoutDataError()

        selector = '[class="mb-0 price-destaque"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '[id="descricao"]'
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
    url = 'https://www.saraiva.com.br/box-o-essencial-da-psicologia-3-volumes-10081856/p'
    scraping_result = ScrapingSaraiva(url).consult()
    # without description
    # scraping_result = scraping_saraiva('https://www.saraiva.com.br/sobre-a-brevidade-da-vida-edicao-especial-com-prefacio-de-lucia-helena-galvao-maya--capa-es-20086735/p')
    print(scraping_result)
