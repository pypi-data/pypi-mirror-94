import urllib3
import os
import json
from kubert import Config
from types import SimpleNamespace

class Client(object):

  def __init__(self, config, poolSize=os.cpu_count()):
    super(Client, self).__init__()
    if config is None:
      config = Config()
    self.config = config
    
    self._HTTPPool = urllib3.connectionpool.connection_from_url(
      'https://' + self.config.host + ':' + self.config.tcpPort, 
      maxsize=poolSize,
      ca_certs = self.config.cert
    )

    self.headers = {
      'Authorization': 'Bearer ' + self.config.token
    }

    self._dicoverResources()

  def request(self, *args, **kwargs):
    kwargs['headers'] = self.headers
    return self._HTTPPool.request(*args, **kwargs)

  def _dicoverResources(self):
    self._apiResources = {}  
    self._apiResources['core'] = {}
    self._apiResources['core']['v1'] = json.loads(self.request("GET", "/api/v1").data)['resources']

    for s in json.loads(self.request("GET", "/apis/apiregistration.k8s.io/v1/apiservices").data)['items']:
      if 'group' not in s['spec']:
        continue
      endpoint = "/apis/" + s['spec']['group'] + "/" + s['spec']['version']
      r = json.loads(self.request("GET", endpoint).data)
      if s['spec']['group'] not in self._apiResources:
        self._apiResources[s['spec']['group']] = {} 
      self._apiResources[s['spec']['group']][s['spec']['version']] = r['resources']
    
    self.resources = {}

    for s in self._apiResources:
      for v in self._apiResources[s]:
        for r in self._apiResources[s][v]:
          if s == 'core':
            endpoint = "/api/%s" % (v)
          else:
            endpoint = "/apis/%s/%s" % (s,v)
          if r['kind'] not in self.resources:
            self.resources[r['kind']] = {}
          if v not in self.resources[r['kind']]:
            self.resources[r['kind']][v] = []
          self.resources[r['kind']][v].append({
            'name': r['name'],
            'singularName': r['name'],
            'namespaced': r['namespaced'],
            'verbs': r['verbs'],
            'group': s
          })

  def resourceExist(self, resource, version="v1"):
    if resource not in self.resources:
      return False
    elif version not in self.resources[resource]:
      return False
    else:
      return True

  def getEndpoints(self, resource, verb, name=None, namespace=None, version="v1"):
    if not self.resourceExist(resource,version):
      print("Couldn't find resource", self._apiResources)
      return None
    resources = self.resources[resource][version]
    endpoints = []
    for r in resources:
      endpoint = ""
      if verb in r['verbs']:
        if r['group'] == 'core':
          endpoint += "/api/"
        else:
          endpoint += "/apis/"+r['group']+"/"
        endpoint += version+"/"
        if namespace is not None:
          endpoint += "namespaces/" + namespace + "/" + r['name']
        else:
          endpoint += r['name']
        if name is not None:
          endpoint += "/" + name 
        endpoints.append(endpoint)
    return endpoints

  def list(self, resource, namespace="default", version="v1"):
    listEndpoints = self.getEndpoints(resource, 'list', namespace=namespace, version=version)
    results =[]
    for e in listEndpoints:
      if not  (e.endswith('/status') or e.endswith('/log')):
        r = json.loads(self.request("GET", e).data, object_hook=lambda d: SimpleNamespace(**d))
        results.append(r)
    if len(results) == 1:
      return results[0]
    return results

  def get(self, resource, name, namespace="default", version="v1"):
    itemEndpoints = self.getEndpoints(resource, 'get', name=name, namespace=namespace, version=version)
    results =[]
    for e in itemEndpoints:
      if not (e.endswith('/status/'+name) or e.endswith('/log/'+name)):
        r = json.loads(self.request("GET", e).data, object_hook=lambda d: SimpleNamespace(**d))
        results.append(r)
    if len(results) == 1:
      return results[0]
    return results

  def watch(self, resource, name=None, namespace=None, version="v1"):
    watchEndpoint = self.getEndpoints(resource, 'watch', name=name, namespace=namespace, version=version)[0]
    r = self.request('GET', watchEndpoint+"?watch=1",  preload_content=False)
    return r


    
      



    
      
  