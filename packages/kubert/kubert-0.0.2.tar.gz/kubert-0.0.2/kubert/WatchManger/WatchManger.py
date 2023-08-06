import json
import logging
import sys
from types import SimpleNamespace
from threading import Thread

class WatchManager(object):

  def __init__(self, client) -> None:
      super().__init__()
      self._client = client
      self._watchers = {}
      self.logger = logging.getLogger(__name__)
      self.logger.setLevel(logging.DEBUG)
      self.logger.addHandler(logging.StreamHandler(sys.stdout))


  def addWatcher(self, watcherName, resource, 
    resourceName=None, 
    namespace=None, 
    version="v1", 
    addedCB=None, 
    modifiedCB=None, 
    deletedCB=None
    ):
    watcher = self._client.watch(resource, name=resourceName, namespace=namespace, version=version)
    self._watchers[watcherName] = objectWatcher(watcher, self.logger,
      added=addedCB, 
      modified=modifiedCB, 
      deleted=deletedCB
    )
    self._watchers[watcherName].start()
    return True

  def registerCallbacks(self, watcherName, added=None, modified=None, deleted=None):
    self._watchers[watcherName].registerCallbacks(added=added, modified=modified, deleted=deleted)
    return True

class objectWatcher(Thread):
  def __init__(self, watcher, logger, **kwargs) -> None:
      super().__init__()
      self._watcher = watcher
      self._logger = logger
      self._callbacks = {
        'added': [],
        'modified': [],
        'deleted': []
      }
      self.registerCallbacks(**kwargs)

  # Borrowed from https://github.com/kubernetes-client/python-base/blob/4bf72d7f0dda1ecfb4a2e02f70cf9bcc700641a4/watch/watch.py
  def _iter_resp_lines(self, resp):
    prev = ""
    for seg in resp.read_chunked(decode_content=False):
        if isinstance(seg, bytes):
            seg = seg.decode('utf8')
        seg = prev + seg
        lines = seg.split("\n")
        if not seg.endswith("\n"):
            prev = lines[-1]
            lines = lines[:-1]
        else:
            prev = ""
        for line in lines:
            if line:
                yield line

  def run(self):
    for e in self._iter_resp_lines(self._watcher):
      o =json.loads(e, object_hook=lambda d: SimpleNamespace(**d))
      self._logger.debug("type: %s -> %s:%s" % (o.type, o.object.metadata.selfLink, o.object.metadata.resourceVersion))
      if len(self._callbacks[o.type.lower()]) > 0:
        for cb in self._callbacks[o.type.lower()]:
          cb(self, o)
      else:
       self._logger.debug("No Callbacks found for %s" % (o.type.lower()))

    print("Thread Exited")

  def registerCallbacks(self, added=None, modified=None, deleted=None):
    if added is not None:
      self._callbacks['added'].append(added)
    if modified is not None:
      self._callbacks['modified'].append(modified)
    if deleted is not None:
      self._callbacks['deleted'].append(deleted)
    return True