
import os
import urllib.parse
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
from mimetypes import guess_extension

import requests

from .interface import WebContentDownloader

class SimpleDownloader(WebContentDownloader):
  """
  하나의 이미지를 다운로드 할 때 사용하는 클래스
  """

  def __init__(self, base, path, 
    headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    self.base = base
    self.path = path
    self.headers = headers
    self.file_id = 0
  
  def get(self, url):
    self.file_id += 1
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
    if compress:
      path = os.path.join(self.path, f'{self.file_id}.zip')
      file = self.compress(url)
      with open(path, 'wb') as f:
        f.write(file.getvalue())
        print(path)
    else:
      response = self.get(url)
      ext = guess_extension(response['content-type'])
      path = os.path.join(self.path, f'{self.file_id}{ext}')
      with open(path, 'wb') as f:
        f.write(response['content'])
        print(path)