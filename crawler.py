import json
import os
import random
import sys
import tempfile
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import (
    NoAlertPresentException, NoSuchWindowException, TimeoutException
)


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
    elem = None
    body = driver.find_elements_by_tag_name('body')
    assert len(body) == 1
    body = body[0]

    buttons = body.find_elements_by_tag_name('button')
    links = body.find_elements_by_tag_name('a')
    inputs = body.find_elements_by_tag_name('input')
    children = buttons + links + inputs

    random.shuffle(children)

    for child in children:
        # Get all the attributes of the child.
        child_attributes = get_all_attributes(driver, child)

        # If the element is not displayed or is disabled, the user can't interact with it. Skip
        # non-displayed/disabled elements, since we're trying to mimic a real user.
        if not child.is_displayed() or not child.is_enabled():
            continue

        elem = child
        break

    if elem is None:
        return None

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
        else:
            raise Exception('Unsupported input type: %s' % input_type)

    close_all_windows_except_first(driver)

    return child_attributes


def get_all_attributes(driver, child):
    child_attributes = driver.execute_script("""
      let elem_attribute = {};

      for (let i = 0; i < arguments[0].attributes.length; i++) {
        elem_attribute[arguments[0].attributes[i].name] = arguments[0].attributes[i].value;
      }
      return elem_attribute;
    """, child)

    return child_attributes


def run(website, driver):
    print('Running {}'.format(website))

    try:
        driver.get(website)
    except TimeoutException as e:
        # Ignore timeouts, as they are too frequent.
        traceback.print_exc()
        print('Continuing...')

    saved_sequence = []
    try:
        for i in range(0, 7):
            elem_attributes = do_something(driver)
            if elem_attributes is None:
                print('Can\'t find any element to interact with on {}'.format(website))
                break
            saved_sequence.append(elem_attributes)

            print('  - Using {}'.format(elem_attributes))
    except TimeoutException as e:
        # Ignore timeouts, as they are too frequent.
        traceback.print_exc()
        print('Continuing...')

    return saved_sequence


def run_all(driver):
    set_timeouts(driver)

    websites = ['https://www.mozilla.org/']

    for i, website in enumerate(websites):
        if os.path.exists('data/{}.txt'.format(i)):
            continue

        try:
            sequence = run(website, driver)

            with open('data/{}.txt'.format(i), 'w') as f:
                for element in sequence:
                    f.write(json.dumps(element) + '\n')

        except:  # noqa: E722
            traceback.print_exc()
            close_all_windows_except_first(driver)

    driver.quit()


# Environmental vars set to overwrite default location of .gcda files
if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    prefix = '/builds/worker/workspace/build/src/'
    strip_count = prefix.count('/')
elif sys.platform.startswith('cygwin') or sys.platform.startswith('win32'):
    prefix = 'z:/build/build/src/'
    strip_count = prefix.count('/') + 1

# Remove a prefix from the path where .gcda files are stored
os.environ['GCOV_PREFIX_STRIP'] = str(strip_count)

# Returns absolute path for created temp file
gcov_dir = tempfile.mkdtemp()
os.environ['GCOV_PREFIX'] = gcov_dir
# Environment variable for JS engine to emit JS coverage information
jsvm_dir = tempfile.mkdtemp()
os.environ['JS_CODE_COVERAGE_OUTPUT_DIR'] = jsvm_dir
os.environ['PATH'] += os.pathsep + os.path.abspath('tools')
os.environ['MOZ_HEADLESS'] = '1'

# Webdriver uses Firefox Binaries from downloaded cov build
driver = webdriver.Firefox(firefox_binary='tools/firefox/firefox-bin')

run_all(driver)
