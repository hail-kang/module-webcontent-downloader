import os
import abc
import urllib.parse
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
from mimetypes import guess_extension

import requests
from bs4 import BeautifulSoup as bs

class WebContentDownloader(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def __init__(self):
    pass

  @abc.abstractmethod
  def get(self):
    pass

  @abc.abstractmethod
  def compress(self):
    pass

  @abc.abstractmethod
  def download(self):
    pass

class SimpleDownloader(WebContentDownloader):

  def __init__(self, base, path, 
    header={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    self.base = base
    self.path = path
    self.headers = header
    self.file_id = 1
  
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
    response = self.get(url)
    ext = guess_extension(response['content-type'])

    file = BytesIO()
    zf = ZipFile(file, 'w')
    zf.writestr(f'{self.file_id}{ext}', response['content'])
    
    return file

  def download(self, url, compress=False):
    url = urllib.parse.urljoin(self.base, url)
    if compress:
      file = self.compress(url)
      path = os.path.join(self.path, f'{self.file_id}.zip')
      with open(path, 'wb') as f:
        f.write(file.getvalue())
    else:
      response = self.get(url)
      ext = guess_extension(response['content-type'])
      path = os.path.join(self.path, f'{self.file_id}{ext}')
      with open(path, 'wb') as f:
        f.write(response['content'])

class SelectorCommand:
  
  def __init__(self, element_title, element_img, attr_src):
    self.title = element_title
    self.img = element_img
    self.src = attr_src

class SelectorDownloader(WebContentDownloader):

  def __init__(self, base, path, 
    header={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    self.base = base
    self.path = path
    self.headers = header
    self.downloader = SimpleDownloader(base, path, header)

  def get(self, url):
    pass