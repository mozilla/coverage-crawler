import os
import tarfile

import taskcluster

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


# Retrieving task from index
index = taskcluster.Index()
taskId = index.findTask('gecko.v2.mozilla-central.' +
                        'latest.firefox.linux64-ccov-opt')['taskId']
# taskId uniquelly identifies artifact
name = os.path.join('ccov-artifacts', taskId +
                    'artifacts.public.build.target.tar.bz2')
# Retrieving artifact
urlretrieve('https://index.taskcluster.net/v1/task/gecko.v2.' +
            'mozilla-central.latest.firefox.linux64-ccov-opt/' +
            'artifacts/public/build/target.tar.bz2', name)
# Extracting artifact
with tarfile.open(name, 'r:bz2') as tar:
    tar.extractall()
os.remove(name)
