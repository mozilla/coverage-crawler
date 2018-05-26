# -*- coding: utf-8 -*-

import os
import platform
import sys
import tarfile
import zipfile

import requests
import taskcluster

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def get_github_release_url(repo_slug):
    repos_url = 'https://api.github.com/repos/{}/releases/latest'.format(repo_slug)
    download_url = 'https://github.com/{}/releases/download/'.format(repo_slug)
    latest_version = requests.get(repos_url)
    data = latest_version.json()
    tag_name = data['tag_name']
    return download_url, tag_name


# Create 'tools/' directory if doesn't exist
if not os.path.exists('tools'):
    os.makedirs('tools')

index = taskcluster.Index()
queue = taskcluster.Queue()

taskId = index.findTask('gecko.v2.mozilla-central.' +
                        'latest.firefox.linux64-ccov-debug')['taskId']

# Download artifacts
for name in ['target.tar.bz2', 'target.code-coverage-gcno.zip', 'chrome-map.json']:
    url = queue.buildUrl('getLatestArtifact', taskId, 'public/build/{}'.format(name))
    urlretrieve(url, os.path.join('tools', name))

# Geckodriver base url fot the latest version
download_url, tag_name = get_github_release_url('mozilla/geckodriver')
geckodriver_url = download_url + tag_name + '/geckodriver-' + tag_name + '-'

# Grcov latest version base url
download_url, tag_name = get_github_release_url('marco-c/grcov')
grcov_url = download_url + tag_name

# OS information for correct geckodriver version
bitness = platform.architecture()[0]

# Complete urls according to platforms
if sys.platform.startswith('linux'):
    grcov_url += '/grcov-linux-x86_64.tar.bz2'
    if bitness == '64bit':
        version = 'linux64.tar.gz'
    else:
        version = 'linux32.tar.gz'
elif sys.platform.startswith('darwin'):
    grcov_url += '/grcov-osx-x86_64.tar.bz2'
    version = 'macos.tar.gz'
elif sys.platform.startswith('cygwin') or sys.platform.startswith('win32'):
    grcov_url += '/grcov-win-x86_64.tar.bz2'
    if bitness == '64bit':
        version = 'win64.zip'
    else:
        version = 'win32.zip'

# Download geckodriver
geckodriver_archive = os.path.join('tools', version)
geckodriver_url += version
urlretrieve(geckodriver_url, geckodriver_archive)

# Download grcov
grcov_archive = os.path.join('tools', 'grcov.tar.bz2')
urlretrieve(grcov_url, grcov_archive)

# Extract and delete archives for artifacts
for filename in ['tools/target.code-coverage-gcno.zip', 'tools/target.tar.bz2', geckodriver_archive, grcov_archive]:
    if filename.endswith('zip'):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(path='tools')
    elif filename.endswith('tar.gz') or filename.endswith('tar.bz2'):
        if filename.endswith('tar.gz'):
            mode = 'r:gz'
        else:
            mode = 'r:bz2'
        with tarfile.open(filename, mode) as tar:
            tar.extractall(path='tools')
    os.remove(filename)
