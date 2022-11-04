# -*- coding: utf-8 -*-

import json
import os
import random
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
from typing import Set

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webelement import FirefoxWebElement

from coverage_crawler import diff
from coverage_crawler import filterpaths
from coverage_crawler import generatehtml

already_clicked_elems = set()


def set_timeouts(driver):
    driver.set_script_timeout(30)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(30)


def wait_loaded(driver):
    try:
        driver.execute_async_script("""
          let done = arguments[0];

          window.onload = done;
          if (document.readyState === "complete") {
            done();
          }
        """)
    except:  # noqa: E722
        traceback.print_exc(file=sys.stderr)
        print('Continuing...')

    # We hope the page is fully loaded in 7 seconds.
    time.sleep(7)

    try:
        driver.execute_async_script("""
          window.requestIdleCallback(arguments[0], {
            timeout: 60000
          });
        """)
    except:  # noqa: E722
        traceback.print_exc(file=sys.stderr)
        print('Continuing...')


def close_all_windows_except_first(driver):
    windows = driver.window_handles

    for window in windows[1:]:
        driver.switch_to.window(window)
        driver.close()

    while True:
        try:
            alert = driver.switch_to.alert()
            alert.dismiss()
        except (NoAlertPresentException, NoSuchWindowException):
            break

    driver.switch_to.window(windows[0])


def find_children(driver: webdriver.Firefox):
    body = driver.find_elements_by_tag_name('body')
    assert len(body) == 1
    body = body[0]

    body.send_keys(Keys.CONTROL, 0)

    buttons = body.find_elements_by_tag_name('button')
    links = body.find_elements_by_tag_name('a')
    inputs = body.find_elements_by_tag_name('input')
    selects = body.find_elements_by_tag_name('select')
    children = buttons + links + inputs + selects

    random.shuffle(children)

    return children


def find_next_unclicked_element_in_page(driver: webdriver.Firefox, not_clickable_elems: Set):
    """
    relies on global variable `already_clicked_elems` to return the next child that
    was not interacted with yet.
    :param driver: the driver with which we look for a child.
    :param not_clickable_elems: a set of elements which cannot be interacted with.
    :return: None, if all children were interacted with.
    :return: the next interactable child, otherwise.
    """
    children = find_children(driver)

    # If we have clickable elements on which we haven't clicked yet, use them; otherwise, use all elements
    if set(children) - already_clicked_elems > not_clickable_elems:
        children = list(set(children) - already_clicked_elems)

    for child in children:
        # If the element is not displayed or is disabled, the user can't interact with it. Skip
        # non-displayed/disabled elements, since we're trying to mimic a real user.
        if not child.is_displayed() or not child.is_enabled() or child in not_clickable_elems:
            continue

        return child

    return None


def perform_action_on_element(driver: webdriver.Firefox, element: FirefoxWebElement) -> None:
    """
    interact with a given element, e.g. by sending keys or clicking on it.
    :param driver: the driver to be used for interaction.
    :param element: the element to be interacted with.
    :raise: NotImplementedError, if an unsupported element type was found.
    """
    if element.tag_name in ['button', 'a']:
        element.click()
    elif element.tag_name == 'input':
        input_type = element.get_attribute('type')
        if input_type == 'url':
            element.send_keys('http://www.mozilla.org/')
        elif input_type == 'text':
            element.send_keys('marco')
        elif input_type == 'email':
            element.send_keys('prova@email.it')
        elif input_type == 'password':
            element.send_keys('aMildlyComplexPasswordIn2017')
        elif input_type == 'checkbox':
            element.click()
        elif input_type == 'number':
            element.send_keys('3')
        elif input_type in ['submit', 'reset', 'button']:
            element.click()
        elif input_type == 'color':
            driver.execute_script("arguments[0].value = '#ff0000'", element)
        elif input_type == 'search':
            element.clear()
            element.send_keys('quick search')
        elif input_type == 'radio':
            element.click()
        elif input_type == 'tel':
            element.send_keys('1234567890')
        elif input_type == 'date':
            element.send_keys('20000101')
        else:
            raise NotImplementedError(f'Unsupported input type: {input_type}')
    elif element.tag_name == 'select':
        for option in element.find_elements_by_tag_name('option'):
            if option.text != '':
                option.click()
                return


def perform_action_on_page(driver: webdriver.Firefox):
    """
    interact with a single element on the current page, e.g. by sending keys or clicking on it.
    relies on global variable `already_clicked_elems` to interact with the next child that
    was not interacted with yet.
    :param driver: the driver with which we interact.
    :return: None, if there are no clickable items.
    :return: a list of attributes of the last element with which we interacted.
    """
    not_clickable_elems = set()

    while True:
        element = None
        try:
            element = find_next_unclicked_element_in_page(driver, not_clickable_elems)

            if element is None:
                return None

            driver.execute_script('return arguments[0].scrollIntoView();', element)
            time.sleep(1)

            perform_action_on_element(driver, element)
            already_clicked_elems.add(element)
            close_all_windows_except_first(driver)
            return get_all_attributes(driver, element)

        except StaleElementReferenceException:
            # don't mark element as clicked if it was stale.
            traceback.print_exc(file=sys.stderr)
            close_all_windows_except_first(driver)

        except (ElementNotInteractableException, InvalidSelectorException, WebDriverException):
            # Ignore frequent exceptions.
            traceback.print_exc(file=sys.stderr)
            close_all_windows_except_first(driver)
            not_clickable_elems.add(element)


def get_all_attributes(driver, child):
    child_attributes = driver.execute_script("""
      let elem_attribute = {};

      for (let i = 0; i < arguments[0].attributes.length; i++) {
        elem_attribute[arguments[0].attributes[i].name] = arguments[0].attributes[i].value;
      }
      return elem_attribute;
    """, child)

    return child_attributes


def run_in_driver(website, driver):
    print('Running {}'.format(website))

    try:
        driver.get(website)
    except TimeoutException:
        # Ignore timeouts, as they are too frequent.
        traceback.print_exc(file=sys.stderr)
        print('Continuing...')

    saved_sequence = []
    for i in range(0, 20):
        print('Iteration {}'.format(i))
        try:
            elem_attributes = perform_action_on_page(driver)
            if elem_attributes is None:
                print('Cannot find any element to interact with on {}'.format(website))
                break
            saved_sequence.append(elem_attributes)

            print('  - Using {}'.format(elem_attributes))
        except TimeoutException:
            # Ignore frequent Timeout exceptions.
            traceback.print_exc(file=sys.stderr)
            print('Continuing...')

    return saved_sequence


def run(websites):
    # Environmental vars set to overwrite default location of .gcda files
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        prefix = '/builds/worker/workspace/build/src/'
        strip_count = prefix.count('/')
    elif sys.platform.startswith('cygwin') or sys.platform.startswith('win32'):
        prefix = 'z:/build/build/src/'
        strip_count = prefix.count('/') + 1

    # Remove a prefix from the path where .gcda files are stored
    os.environ['GCOV_PREFIX_STRIP'] = str(strip_count)
    os.environ['PATH'] += os.pathsep + os.path.abspath('tools')
    os.environ['MOZ_HEADLESS'] = '1'
    already_clicked_elems.clear()
    # Create temporary directories with context manager
    with tempfile.TemporaryDirectory() as gcov_dir, tempfile.TemporaryDirectory() as jsvm_dir:
        os.environ['GCOV_PREFIX'] = gcov_dir
        os.environ['JS_CODE_COVERAGE_OUTPUT_DIR'] = jsvm_dir

        # Webdriver uses Firefox Binaries from downloaded cov build
        driver = webdriver.Firefox(firefox_binary='tools/firefox/firefox-bin')

        set_timeouts(driver)

        for website in websites:
            # All steps are stored in new folder
            data_folder = str(uuid.uuid4())
            os.makedirs(data_folder, exist_ok=True)
            try:
                sequence = run_in_driver(website, driver)
                with open('{}/steps.txt'.format(data_folder), 'w') as f:
                    f.write('Website name: ' + website + '\n')
                    for element in sequence:
                        f.write(json.dumps(element) + '\n')
            except:  # noqa: E722
                traceback.print_exc(file=sys.stderr)
                close_all_windows_except_first(driver)

        # Add paths to Mozilla-central modules
        sys.path.insert(0, 'tools/mozbuild/codecoverage')
        sys.path.insert(0, 'tools')

        from lcov_rewriter import LcovFileRewriter
        jsvm_files = [os.path.join(jsvm_dir, e) for e in os.listdir(jsvm_dir)]
        rewriter = LcovFileRewriter(os.path.join('tools', 'chrome-map.json'))
        jsvm_output_dir = os.path.join(jsvm_dir, 'jsvm_output')
        os.makedirs(jsvm_output_dir, exist_ok=True)
        jsvm_output_file = os.path.join(jsvm_output_dir, 'jsvm_lcov_output.info')
        rewriter.rewrite_files(jsvm_files, jsvm_output_file, '')

        grcov_command = [
            os.path.join('tools', 'grcov'),
            '-t', 'coveralls+',
            '-p', prefix,
            'tools', gcov_dir,
            jsvm_output_dir,
            '--filter', 'covered',
            '--token', 'UNUSED',
            '--commit-sha', 'UNUSED'
        ]

        with open('output.json', 'w+') as outfile:
            subprocess.check_call(grcov_command, stdout=outfile)

        with open('tests_report.json') as baseline_rep, open('output.json') as rep:
            baseline_report = json.load(baseline_rep)
            report = json.load(rep)

        filterpaths.ignore_third_party_filter(report)

        # Create diff report
        diff_report = diff.compare_reports(baseline_report, report, True)

        with open('{}/diff.json'.format(data_folder), 'w') as outfile:
            json.dump(diff_report, outfile)

        generatehtml.generate_html(data_folder)

        driver.quit()

        return os.path.abspath(os.path.join(os.getcwd(), '{}/report'.format(data_folder)))
