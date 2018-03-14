import tarfile
import os
import taskcluster
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

# Retrieving task from index
index = taskcluster.Index()
taskId = index.findTask('gecko.v2.mozilla-central.' +
                        'latest.firefox.linux64-ccov-opt')['taskId']
# Retrieving artifact from Queue
queue = taskcluster.Queue()
url = queue.buildUrl('getLatestArtifact', taskId,
                     'public/build/target.tar.bz2')
name = os.path.join('ccov-artifacts', taskId +
                    'artifacts.public.build.target.tar.bz2')
urlretrieve(url, name)
# Extracting artifact
with tarfile.open(name, 'r:bz2') as tar:
    tar.extractall()
os.remove(name)
