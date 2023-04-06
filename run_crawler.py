# -*- coding: utf-8 -*-

from coverage_crawler import crawler
from coverage_crawler import github

reports = {}

with open('websites.txt') as f:
    for website in f:
        report = crawler.run(website)
        reports[website] = report

github.upload_to_github(reports, 'GIT_ACCOUNT', 'GIT_PASSWORD')
