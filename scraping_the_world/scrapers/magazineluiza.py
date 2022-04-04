import traceback

from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from parsel import Selector

from scraping_the_world.models.querys import add_log, get_config
from scraping_the_world.scrapers.webdriver_manager.webdriver_manager import WebdriverManager
from scraping_the_world.exceptions.scrapers_exceptions import SiteWhithoutDataError, PageNotFound404Error, PageWithCaptchaError


class ScrapingMaganizeluiza:
    def __init__(self, url):
        self.__url = url
        self.__site_data = {
            'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None, 'error': False}

    def consult(self):
        scraping_type = int(get_config('scraping_magazineluiza'))
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
        except PageWithCaptchaError as error:
            self.__site_data['error'] = error
        except Exception as error:
            add_log(log_text=f'[scraping_magazineluiza] Traceback: {error}', log_type='ERROR')
            self.__site_data['error'] = error
        finally:
            if webdriver_manager:
                webdriver_manager.driver_quit()

            return self.__site_data

    def __scraping_requests(self):
        session = HTMLSession()
        response = session.get(self.__url).text
        parsel_selector = Selector(text=response)

        page_text = 'Não encontramos essa página'
        if page_text in response:
            raise PageNotFound404Error()

        page_text = 'Resolva este CAPTCHA para solicitar o desbloqueio do site'
        if page_text in response:
            raise PageNotFound404Error()

        selector = '[class="header-product__title"]::text'
        self.__site_data['titulo'] = parsel_selector.css(selector).get()

        selector = '.showcase-product__big-img::attr(src)'
        self.__site_data['imagem'] = parsel_selector.css(selector).get()

        selector = '[class="price-template__text"]::text'
        self.__site_data['preco'] = parsel_selector.css(selector).get()

        self.__site_data['descricao'] = 'No Description'

        selector = '[rel="canonical"]::attr(href)'
        self.__site_data['url'] = parsel_selector.css(selector).get()

        return self.__site_data

    def __scraping_selenium(self):
        driver, wdtk = WebdriverManager().get_driver()
        driver.get(self.__url)

        page_text = 'Não encontramos essa página'
        if wdtk.text_is_present(wait_time=2, locator=(By.TAG_NAME, 'html'), text=page_text):
            raise PageNotFound404Error()

        page_text = 'Resolva este CAPTCHA para solicitar o desbloqueio do site'
        if wdtk.text_is_present(wait_time=2, locator=(By.TAG_NAME, 'html'), text=page_text):
            raise PageWithCaptchaError()

        selector = '[class="header-product__title"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['titulo'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        selector = '.showcase-product__big-img'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['imagem'] = driver.find_element(By.CSS_SELECTOR, selector).get_attribute('src')
        else:
            raise SiteWhithoutDataError()

        selector = '[class="price-template__text"]'
        if wdtk.element_is_present(wait_time=10, locator=(By.CSS_SELECTOR, selector)):
            self.__site_data['preco'] = driver.find_element(By.CSS_SELECTOR, selector).text
        else:
            raise SiteWhithoutDataError()

        self.__site_data['descricao'] = 'No Description'

        self.__site_data['url'] = driver.current_url

        return self.__site_data


if __name__ == '__main__':
    ...
    # no description
    url = 'https://www.magazineluiza.com.br/papel-fotografico-a4-180g-glossy-branco-brilhante-resistente-a-agua-100-folhas-premium/p/ke2bb2cj82/cf/ppft/'
    # 404Page
    # url = 'https://www.magazineluiza.com.br/tv-4dddddk-ulddtra-hd/tv-ddddde-vidsseo/ss/sset/tv4444k/'
    scraping_result = ScrapingMaganizeluiza(url).consult()  # with description
    print(scraping_result)
