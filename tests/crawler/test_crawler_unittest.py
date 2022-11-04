# encoding: utf-8
import multiprocessing
import unittest

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.firefox import GeckoDriverManager

from coverage_crawler import crawler
from tests.example_website import website_app
from tests.example_website.website_app import WEBSITE_TITLE
from tests.example_website.website_app import run_server


class TestCrawler(unittest.TestCase):
    driver: webdriver.Firefox

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_close_all_windows_except_first(self):
        """
        when multiple windows are open,
        verify that calling `close_all_windows_except_first` closes all except the first.
        """
        _open_tab_script = 'window.open("", "new window")'
        self.driver.execute_script(_open_tab_script)
        assert (len(self.driver.window_handles) == 2), 'some windows were not opened properly.'

        crawler.close_all_windows_except_first(self.driver)

        assert (len(self.driver.window_handles) == 1), 'some windows were not closed properly.'


class TestCrawlerLive(unittest.TestCase):
    SERVER_SETUP_TRIES = 10

    @classmethod
    def setUpClass(cls):
        cls.server = multiprocessing.Process(target=run_server)
        cls.server.start()

        for try_id in range(cls.SERVER_SETUP_TRIES):
            try:
                print(f'class setup tries: {try_id}/{cls.SERVER_SETUP_TRIES}')
                with webdriver.Firefox(executable_path=GeckoDriverManager().install()) as test_driver:
                    test_driver.get(website_app.WEBSITE_URL)
                    assert test_driver.title == WEBSITE_TITLE

                return
            except WebDriverException as e:
                print('got exception:', e)

        cls.server.terminate()
        cls.server.join()
        cls.fail(cls, 'website did not start up correctly.')

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.join()

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_find_children(self):
        """
        when example server is open,
        verify that `find_children` returns the expected children.
        """
        expected_link_text = 'i am the first link in the first div'

        self.driver.get(website_app.WEBSITE_URL)
        assert (self.driver.title == WEBSITE_TITLE), f'incorrect driver title: {self.driver.title}'

        children = crawler.find_children(self.driver)
        num_children = len(children)
        assert (num_children == 1), f'incorrect number of children found: {num_children}'
        assert (children[0].text == expected_link_text)

    def test_get_all_attributes(self):
        """
        when example server is open,
        verify that `get_all_attributes` returns the expected attributes.
        """
        expected_attribute = 'href'

        self.driver.get(website_app.WEBSITE_URL)
        assert (self.driver.title == WEBSITE_TITLE), f'incorrect driver title: {self.driver.title}'

        child = crawler.find_children(self.driver)[0]
        attributes = crawler.get_all_attributes(self.driver, child)
        num_attributes = len(attributes)
        assert (num_attributes == 1), f'incorrect number of attributes found: {num_attributes}'
        assert (expected_attribute in attributes), f'expected attribute is missing: {expected_attribute}'
