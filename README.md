# coverage-crawler
[![Build Status](https://travis-ci.org/marco-c/coverage-crawler.svg?branch=master)](https://travis-ci.org/marco-c/coverage-crawler)

A crawler to find websites that exercise code in Firefox that is not covered by unit tests

## Usage on local machine

- Create and activate Python 3.6 virtual environment
- In the virtual environment install requirements for the project running `pip install -r requirements`
- To install testing utilities run `pip install -r test-requirements.txt`
- If you want to test Python file with Flake8 run `flake8 name_or_file.py`
- run `latest_cov_build.py` to download the latest coverage build of Firefox
- run `crawler.py` 
