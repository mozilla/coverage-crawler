# -*- coding: utf-8 -*-

import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import uuid

import codecoverage
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException

import diff


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

    driver.execute_script('return arguments[0].scrollIntoView();', elem)
    time.sleep(1)

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
        elif input_type == 'submit':
            elem.click()
        elif input_type == 'color':
            driver.execute_script("arguments[0].value = '#ff0000'", elem)
        elif input_type == 'search':
            elem.clear()
            elem.send_keys('quick search')
        else:
            raise Exception('Unsupported input type: %s' % input_type)
    elif elem.tag_name == 'select':
        for option in elem.find_elements_by_tag_name('option'):
            if option.text != '':
                option.click()
                break

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
        for i in range(0, 20):
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


def run_all(driver, data_folder):
    set_timeouts(driver)

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    with open('websites.txt') as f:
        for i, website in enumerate(f):
            if os.path.exists('{}/{}.txt'.format(data_folder, i)):
                continue

            try:
                sequence = run(website, driver)

                with open('{}/{}.txt'.format(data_folder, i), 'w') as f:
                    f.write('Website name: ' + website + '\n')
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
os.environ['PATH'] += os.pathsep + os.path.abspath('tools')
os.environ['MOZ_HEADLESS'] = '1'

# create a temporary directory using the context manager
with tempfile.TemporaryDirectory() as gcov_dir, tempfile.TemporaryDirectory() as jsvm_dir:
    os.environ['GCOV_PREFIX'] = gcov_dir
    os.environ['JS_CODE_COVERAGE_OUTPUT_DIR'] = jsvm_dir

    # Webdriver uses Firefox Binaries from downloaded cov build
    driver = webdriver.Firefox(firefox_binary='tools/firefox/firefox-bin')

    # All steps are stored in new folder
    data_folder = str(uuid.uuid4())
    run_all(driver, data_folder)

    sys.path.insert(0, 'tools/mozbuild/codecoverage')

    from lcov_rewriter import LcovFileRewriter

    jsvm_output_file = 'jsvm_lcov_output.info'
    jsvm_files = [os.path.join(jsvm_dir, e) for e in os.listdir(jsvm_dir)]
    rewriter = LcovFileRewriter(os.path.join('tools', 'chrome-map.json'))
    rewriter.rewrite_files(jsvm_files, jsvm_output_file, '')

    # Zip gcda file from gcov directory
    shutil.make_archive('code-coverage-gcda', 'zip', gcov_dir)
    grcov_command = [
        os.path.join('tools', 'grcov'),
        '-t', 'coveralls+',
        '-p', prefix,
        os.path.join('tools', 'target.code-coverage-gcno.zip'), 'code-coverage-gcda.zip',
        jsvm_output_file,
        '--filter', 'covered',
        '--token', 'UNUSED',
        '--commit-sha', 'UNUSED'
    ]

    with open('output.json', 'w+') as outfile:
        subprocess.check_call(grcov_command, stdout=outfile)

    with open('tests_report.json') as baseline_rep, open('output.json') as rep:
        baseline_report = json.load(baseline_rep)
        report = json.load(rep)

    # Create diff report
    diff_report = diff.compare_reports(baseline_report, report, True)
    with open('{}/diff.json'.format(data_folder), 'w') as outfile:
        json.dump(diff_report, outfile)

    for filename in ['code-coverage-gcda.zip', jsvm_output_file]:
        os.remove(filename)

    with open('{}/diff.json'.format(data_folder), 'r') as report:
        parsed_json = json.load(report)

    file_obj = open('{}/report.info'.format(data_folder), 'w')

    source_files = parsed_json['source_files']

    file_obj.write('TN\n')
    for source_file in source_files:
        file_obj.write('SF:{}\n'.format(source_file['name']))
        executed = 0

        # Functions
        if len(source_file['functions']) != 0:
            for function in source_file['functions']:
                file_obj.write('FN:{},{}\n'.format(function['start'], function['name']))
            for function in source_file['functions']:
                if function['exec'] is True:
                    file_obj.write('FNDA:{},{}\n'.format(1, function['name']))
                    executed += 1
                else:
                    file_obj.write('FNDA:{},{}\n'.format(0, function['name']))
        file_obj.write('FNF:{}\n'.format(len(source_file['functions'])))
        file_obj.write('FNH:{}\n'.format(executed))

        # Branches
        branch_hits = 0
        if len(source_file['branches']) != 0:
            for branch in source_file['branches']:
                if branch['taken'] is True:
                    file_obj.write('BRDA:{},0,{},{}\n'.format(branch['line'], branch['number'], 1))
                    branch_hits += 1
                else:
                    file_obj.write('BRDA:{},0,{},{}\n'.format(branch['line'], branch['number'], '-'))
        file_obj.write('BRF:{}\n'.format(len(source_file['branches'])))
        file_obj.write('BRH:{}\n'.format(branch_hits))

        # Lines
        line_number = 0
        cov_line_count = 0
        if len(source_file['coverage']) != 0:
            for line in source_file['coverage']:
                line_number += 1
                if line is not None:
                    file_obj.write('DA:{},{}\n'.format(line_number, line))
                    if line > 0:
                        cov_line_count += 1
        file_obj.write('LF:{}\n'.format(len(source_file['coverage'])))
        file_obj.write('LH:{}\n'.format(cov_line_count))
        file_obj.write('end_of_record\n')
    file_obj.close()

    codecoverage.download_genhtml()

    ret = subprocess.call(['lcov-bin/usr/local/bin/genhtml', '-o', os.path.join(data_folder, 'report'), '--show-details', '--highlight', '--ignore-errors', 'source', '--legend', os.path.join(data_folder, 'report.info'), '--prefix', 'tools/firefox'])

    if ret != 0:
        raise Exception('Error while running genhtml.')
