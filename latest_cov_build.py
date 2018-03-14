<<<<<<< 835b3e8d057109aebc9eaf465a0e161a305c71f7
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
=======
import tarfile
import sys
import os
import taskcluster
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib import urlencode, urlretrieve
    from urllib2 import urlopen


index = taskcluster.Index()
queue = taskcluster.Queue()
route = "gecko.v2.mozilla-central.latest.firefox.linux64-ccov-opt"
taskId = index.findTask(route)['taskId']
artifactName = 'public/build/target.tar.bz2'
name = os.path.join('ccov-artifacts', taskId +
                    'artifacts.public.build.target.tar.bz2')
url = queue.buildUrl('getLatestArtifact', taskId, artifactName)
print(url)
urlretrieve(url, name)
tar = tarfile.open(name, 'r:bz2')
tar.extractall()
tar.close()
<<<<<<< a961cb16170f75fe519d6a89a38059380a8465cb
# target.tar.bz2 deleted
>>>>>>> download the latest Firefox coverage build
=======
>>>>>>> implemented with taskcluster API
os.remove(name)
