import os
import traceback

from selenium import webdriver
from selenium_stealth import stealth

from scraping_the_world.scrapers.webdriver_manager.webdriver_toolkit import WebDriverToolKit
from scraping_the_world.models.querys import add_log
from env import ENV

WEBDRIVERS_PATH = os.path.dirname(os.path.realpath(__file__))


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WebdriverManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__driver = None

    def get_driver(self):
        if not self.__driver:
            self.__driver = self.create_driver()

        wdtk = WebDriverToolKit(self.__driver)
        return self.__driver, wdtk

    def create_driver(self):
        try:
            options = self.__get_options()
            if ENV['ENV'] == 'DEV':
                if int(ENV['SELENIUM_REMOTE']) == 1:
                    self.__driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
                else:
                    webdriver_path = f'{WEBDRIVERS_PATH}\\chromedriver'
                    self.__driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
            else:
                self.__driver = webdriver.Remote(command_executor='http://container_selenium:4444/wd/hub', options=options)

            self.__driver.maximize_window()

            stealth(driver=self.__driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
            return self.__driver
        except:
            traceback.print_exc()
            add_log(log_text=f'[WebdriverManager] Traceback: {traceback.format_exc()}', log_type='ERROR')

    @staticmethod
    def __get_options():
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')

        options.add_argument('--incognito')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--enable-automation')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_argument(
        #     '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36')

        # options.add_argument('--headless')
        return options

    def driver_quit(self):
        try:
            if self.__driver:
                self.__driver.quit()
                self.__driver = None
        except:
            traceback.print_exc()
            add_log(log_text=f'[WebdriverManager] Traceback: {traceback.format_exc()}', log_type='ERROR')
