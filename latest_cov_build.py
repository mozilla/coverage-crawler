<<<<<<< c37f3812229c1a1a3d771aa145c747a73b41cafb
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
=======
>>>>>>> flake isort imports cleanup
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
<<<<<<< 4c96a85728db505594bc213bd2608e280d40ebed
urlretrieve(url, name)
<<<<<<< 8b47a9f09fcbb0ec4d978d66b1061afde1554a0f
<<<<<<< c43ebd63c26dd0a52d2fb192873e0cd6fdbbe52f
tar = tarfile.open(name, 'r:bz2')
tar.extractall()
tar.close()
<<<<<<< a961cb16170f75fe519d6a89a38059380a8465cb
# target.tar.bz2 deleted
>>>>>>> download the latest Firefox coverage build
=======
>>>>>>> implemented with taskcluster API
=======
=======
=======
# Retrieving artifact
urlretrieve('https://index.taskcluster.net/v1/task/gecko.v2.' +
            'mozilla-central.latest.firefox.linux64-ccov-opt/' +
            'artifacts/public/build/target.tar.bz2', name)
>>>>>>> changed urlretreve arguments
# Extracting artifact
>>>>>>> sections added
with tarfile.open(name, 'r:bz2') as tar:
    tar.extractall()
>>>>>>> added context manager, checked with flake8
os.remove(name)
