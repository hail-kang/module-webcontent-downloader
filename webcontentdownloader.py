import os
import abc
import urllib.parse
from datetime import datetime
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup as bs

class WebContentDownloader(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def __init__(self, base, path, header):
    self.base = base
    self.path = path

  @abc.abstractmethod
  def get(self, url):
    pass

  @abc.abstractmethod
  def compress(self, url):
    pass

  @abc.abstractmethod
  def download(self, url, name, compress=False):
    pass

class SimpleDownloader(WebContentDownloader):

  def __init__(self, base, path, 
    header={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    self.base = base
    self.path = path
    self.headers = header
  
  def get(self, url):
    url = urllib.parse.urljoin(self.base, url)
    response = requests.get(url, headers=self.headers)
    if response.ok:
      return {
        'status': response.status_code,
        'content': response.content,
        'content-type': response.headers.get('content-type')
      }
    else:
      raise Exception('not 200 error') 

  def compress(self, url):
    url = urllib.parse.urljoin(self.base, url)
    pass

  def download(self, url, name, compress=False):
    url = urllib.parse.urljoin(self.base, url)
    if compress:
      response = self.get(url)
      path = os.path.join(self.path, name)
      with ZipFile(path, 'w') as zf:
        zf.writestr(name, response['content'])
    else:
      response = self.get(url)
      path = os.path.join(self.path, name)
      with open(path, 'wb') as f:
        f.write(response['content'])