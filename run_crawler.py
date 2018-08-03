# -*- coding: utf-8 -*-

from coverage_crawler import crawler
from coverage_crawler import github

with open('websites.txt') as f:
    for website in f:
        report = crawler.run(website)
        github.upload_to_github(report)
