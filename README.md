# coverage-crawler
[![Build Status](https://travis-ci.org/mozilla/coverage-crawler.svg?branch=master)](https://travis-ci.org/mozilla/coverage-crawler)

A crawler to find websites that exercise code in Firefox that is not covered by unit tests

## Software requirements

- You will need python>=3.6, pip for python>=3.6 and [Mercurial](https://www.mercurial-scm.org/) source control management tools installed on your machine to run the script.

- For easy environment setup, please take a look at `/easy-environment-setup` folder.

## Usage as a script

- Install requirements with `pip install -r requirements.txt`;
- Install development requirements with `pip install -r test-requirements.txt`;
- Run the `download_artifacts.py` script with the desired revision passed as argument to download the latest Firefox coverage build;
- Run the `run_crawler.py` script.

## Usage as a module

- Add this project's repository to your requirements file as a Git dependency;
- Import `coverage_crawler`;
- Use function `download_artifacts` from `latest_cov_build.py` with the desired revision passed as argument to download the latest Firefox coverage build and other artifacts;
- Run function `run` from `crawler.py` with the desired website passed as an argument.
