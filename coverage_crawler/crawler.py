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

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

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
        traceback.print_exc()
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
        traceback.print_exc()
        print('Continuing...')


def close_all_windows_except_first(driver):
    windows = driver.window_handles

    for window in windows[1:]:
        driver.switch_to_window(window)
        driver.close()

    while True:
        try:
            alert = driver.switch_to_alert()
            alert.dismiss()
        except (NoAlertPresentException, NoSuchWindowException):
            break

    driver.switch_to_window(windows[0])


def do_something(driver):
    not_clickable_elems = set()

    while True:
        elem = None
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

        try:
            # If we have clickable elements on which we haven't clicked yet, use them; otherwise, use all elements
            if set(children) - already_clicked_elems > not_clickable_elems:
                children = list(set(children) - already_clicked_elems)

            for child in children:
                # If the element is not displayed or is disabled, the user can't interact with it. Skip
                # non-displayed/disabled elements, since we're trying to mimic a real user.
                if not child.is_displayed() or not child.is_enabled() or child in not_clickable_elems:
                    continue

                elem = child
                break

            if elem is None:
                return None

            driver.execute_script('return arguments[0].scrollIntoView();', elem)
            time.sleep(1)

            if elem.tag_name in ['button', 'a']:
                elem.click()
            elif elem.tag_name == 'input':
                input_type = elem.get_attribute('type')
                if input_type == 'url':
                    elem.send_keys('http://www.mozilla.org/')
                elif input_type == 'text':
                    elem.send_keys('marco')
                elif input_type == 'email':
                    elem.send_keys('prova@email.it')
                elif input_type == 'password':
                    elem.send_keys('aMildlyComplexPasswordIn2017')
                elif input_type == 'checkbox':
                    elem.click()
                elif input_type == 'number':
                    elem.send_keys('3')
                elif input_type in ['submit', 'reset', 'button']:
                    elem.click()
                elif input_type == 'color':
                    driver.execute_script("arguments[0].value = '#ff0000'", elem)
                elif input_type == 'search':
                    elem.clear()
                    elem.send_keys('quick search')
                elif input_type == 'radio':
                    elem.click()
                elif input_type == 'tel':
                    elem.send_keys('1234567890')
                elif input_type == 'date':
                    elem.send_keys('20000101')
                else:
                    raise Exception('Unsupported input type: %s' % input_type)
            elif elem.tag_name == 'select':
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text != '':
                        option.click()
                        break

            already_clicked_elems.add(elem)

            close_all_windows_except_first(driver)

            # Get all the attributes of the child.
            return get_all_attributes(driver, child)

        except (ElementNotInteractableException, StaleElementReferenceException, InvalidSelectorException, WebDriverException):
            # Ignore frequent exceptions.
            traceback.print_exc()
            not_clickable_elems.add(elem)
            close_all_windows_except_first(driver)


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
    except TimeoutException as e:
        # Ignore timeouts, as they are too frequent.
        traceback.print_exc()
        print('Continuing...')

    saved_sequence = []
    for i in range(0, 20):
        try:
            elem_attributes = do_something(driver)
            if elem_attributes is None:
                print('Can\'t find any element to interact with on {}'.format(website))
                break
            saved_sequence.append(elem_attributes)

            print('  - Using {}'.format(elem_attributes))
        except TimeoutException:
            # Ignore frequent Timeout exceptions.
            traceback.print_exc()
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
                traceback.print_exc()
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
