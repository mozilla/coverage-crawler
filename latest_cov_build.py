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
os.remove(name)
