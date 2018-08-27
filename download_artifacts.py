# -*- coding: utf-8 -*-

import argparse

from coverage_crawler import latest_cov_build

parser = argparse.ArgumentParser()
parser.add_argument('--revision', action='store', nargs='?', help='Optional revision of the build')
args = parser.parse_args()
latest_cov_build.download_artifacts(args.revision)
