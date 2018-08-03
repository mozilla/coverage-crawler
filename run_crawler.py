# -*- coding: utf-8 -*-

from coverage_crawler import crawler

with open('websites.txt') as f:
    for website in f:
        report = crawler.run(website)
