import requests
import json
from easysettings import EasySettings
from pathlib import Path
import tensorflow as tf
import shutil
import os
import zipfile

api_host = 'https://api.inferrd.com'

settings = EasySettings(str(Path.home()) + "/.inferrd.conf")

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            filePath = os.path.join(root, file)
            inZipPath = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
            # remove base folder
            ziph.write(filePath, inZipPath.replace('inferrd-model/', ''))

__all__ = [
    'indextools',
    'doctools'
]

def __main__():
  print('Hi')

def auth(key):
  settings.set('api_key', key)
  settings.save()

def get_model(name):
  api_key = settings.get('api_key')

  r = requests.get(api_host + '/service/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()


def new_version(modelId):
  api_key = settings.get('api_key')

  r = requests.post(api_host + '/service/' + modelId + '/versions', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def deploy_version(versionId):
  api_key = settings.get('api_key')

  r = requests.post(api_host + '/version/' + versionId + '/deploy', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def find_version(modelId, name):
  api_key = settings.get('api_key')

  r = requests.get(api_host + '/service/' + modelId + '/versions/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

# arguments
# includeFailures=True/False
def get_requests(name, **kwargs):
  model = get_model(name)
  api_key = settings.get('api_key')

  includeFailures = False
  version = None
  limit = 100
  page = 0

  if 'limit' in kwargs:
    limit = kwargs['limit']

  if 'page' in kwargs:
    page = kwargs['page']

  if 'includeFailures' in kwargs:
    includeFailures = kwargs['includeFailures']

  if 'version' in kwargs:
    v = find_version(model['id'], kwargs['version'])
    version = v['id']

  url = api_host + '/service/' + model['id'] + '/requests?' + ('responseStatus=200&' if not includeFailures else '') + 'limit=' + str(limit) + '&page=' + str(page) + ('&version=' + version if version else '')

  print(url)

  r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()
      



def deploy_tf(tf_model, name):
  if(settings.get('api_key') == ''):
    print('No api key. Use inferrd.auth() first.')
    exit()

  print('> Saving model to folder')

  if tf_model is None:
    print('Empty tensorflow model. Make sure the first argument is a TensorFlow v2 model.')
    exit()

  model = get_model(name)

  version = new_version(model['id'])

  if os.path.exists('./inferrd-model'):
    shutil.rmtree('./inferrd-model')

  tf.saved_model.save(tf_model, './inferrd-model')
    
  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir('./inferrd-model', zipf) 
  zipf.close()

  # upload to storage
  print('> Uploading model')
  f = open("./model.zip", 'rb')
  r = requests.put(version['signedUpload'], data=f, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  shutil.rmtree('./inferrd-model')
  #os.remove('./model.zip')

  print('> Model deployed')
  return version['id']

  

def get_request_history(apiKey, kwargs):
  print('Getting request')

def call_model(serveKey, payload):
  r = requests.post(api_host + '/infer/' + serveKey, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
  return r.json()