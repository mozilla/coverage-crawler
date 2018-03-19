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


index = taskcluster.Index()
queue = taskcluster.Queue()

taskId = index.findTask('gecko.v2.mozilla-central.' +
                        'latest.firefox.linux64-ccov-opt')['taskId']

# Download artifacts
for name in ['target.tar.bz2', 'target.code-coverage-gcno.zip', 'chrome-map.json']:
    url = queue.buildUrl('getLatestArtifact', taskId, 'public/build/{}'.format(name))
    urlretrieve(url, os.path.join('tools', name))

# Extracting coverage build artifact
with tarfile.open('tools/target.tar.bz2', 'r:bz2') as tar:
    tar.extractall(path='tools')
os.remove('tools/target.tar.bz2')

# Geckodriver download
# OS information for correct geckodriver version
bitness = platform.architecture()[0]
latest_version = requests.get('https://api.github.com/repos/mozilla/geckodriver/releases/latest')
data = latest_version.json()
tag_name = data['tag_name']
base_url = 'https://github.com/mozilla/geckodriver/releases/download/' + tag_name + '/geckodriver-' + tag_name + '-'

# Linux OS
if sys.platform.startswith('linux'):
    if bitness == '64bit':
        version = 'linux64.tar.gz'
    else:
        version = 'linux32.tar.gz'

# MacOS
elif sys.platform.startswith('darwin'):
    version = 'macos.tar.gz'

# Windows or Cygwin
elif sys.platform.startswith('cygwin') or sys.platform.startswith('win32'):
    if bitness == '64bit':
        version = 'win64.zip'
    else:
        version = 'win32.zip'

# Create 'tools/' directory if doesn't exist
if not os.path.exists('tools'):
    os.makedirs('tools')

# Download
name = os.path.join('tools', version)
base_url += version
urlretrieve(base_url, name)

# Extract
if version.endswith('zip'):
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall('tools')

# MacOS and Linux OS have 'tar.gz' extensions
elif base_url.endswith('tar.gz'):
    with tarfile.open(name, 'r:gz') as tar:
        tar.extractall(path='tools')

os.remove(name)
