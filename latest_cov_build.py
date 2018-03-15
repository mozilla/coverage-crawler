import os
import tarfile

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


name = 'latest.artifacts.public.build.target.tar.bz2'

# Retrieving artifact
urlretrieve('https://index.taskcluster.net/v1/task/gecko.v2.' +
            'mozilla-central.latest.firefox.linux64-ccov-opt/' +
            'artifacts/public/build/target.tar.bz2', name)

# Extracting artifact
with tarfile.open(name, 'r:bz2') as tar:
    tar.extractall()
os.remove(name)
