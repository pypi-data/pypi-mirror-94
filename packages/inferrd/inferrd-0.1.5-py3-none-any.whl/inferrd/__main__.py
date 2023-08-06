import sys
from easysettings import EasySettings
from pathlib import Path

settings = EasySettings(str(Path.home()) + "/.inferrd.conf")

def main():
  if(len(sys.argv) <= 1) or (len(sys.argv) > 1 and sys.argv[1] != 'auth'):
    print('The only command available is "auth"')
    exit()

  if(len(sys.argv) == 2):
    print('Missing api key. Usage: inferrd auth <api-key>')
    exit()

  api_key = sys.argv[2]
  settings.set('api_key', api_key)
  settings.save()
  print('API Key has been set.')

if __name__ == '__main__':
  main()