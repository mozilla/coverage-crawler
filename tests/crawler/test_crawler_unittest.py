# encoding: utf-8
import unittest

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

from coverage_crawler import crawler


class TestCrawler(unittest.TestCase):
    driver: webdriver.Firefox

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    def tearDown(self):
        self.driver.close()

    def test_close_all_windows_except_first(self):
        """
        when multiple windows are open,
        verify that calling `close_all_windows_except_first` closes all except the first.
        """
        _open_tab_script = 'window.open("", "new window")'
        self.driver.execute_script(_open_google_tab_script)
        assert (len(self.driver.window_handles) == 2), 'some windows were not opened properly.'

        crawler.close_all_windows_except_first(self.driver)

        assert (len(self.driver.window_handles) == 1), 'some windows were not closed properly.'
