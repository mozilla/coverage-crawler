# -*- coding: utf-8 -*-

import os
import shutil
import subprocess


def upload_to_github(report_path):
    # Clone the repository if doesn't exist
    if not os.path.isdir('coverage-crawler-reports'):
        subprocess.run(['git', 'clone', 'https://github.com/coverage-crawler-updater/coverage-crawler-reports'])
    os.chdir('coverage-crawler-reports')

    # Remove the content of repository except of README
    prev_files = os.listdir(os.getcwd())
    for f in prev_files:
        if f != 'README.md' and f.startswith('.') is False:
            print(f)
    subprocess.run(['git', 'pull', 'https://github.com/rhcu/coverage-crawler-reports', 'master'])

    # Push the new content
    files = os.listdir(os.path.abspath(report_path))
    print(files)
    for f in files:
        print('Im here')
        shutil.move(os.path.join(report_path, f), os.getcwd())

    # Commit the content
    subprocess.run(['git', 'add', '*'])
    subprocess.run(['git', 'commit', '-m', 'Coverage crawler reports upload'])
    subprocess.run(['git', 'push', 'https://coverage-crawler-updater:ACCESS_TOKEN@github.com/coverage-crawler-updater/coverage-crawler-reports', 'master', '--force'])
