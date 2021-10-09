import os
import abc
import urllib.parse
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
from mimetypes import guess_extension

import requests
from bs4 import BeautifulSoup

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


class SelectorCommand:
  
  def __init__(self, element, attribute):
    self.element = element
    self.attribute = attribute

class SelectorDownloader(WebContentDownloader):

  def __init__(self, base, path, 
    header={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    self.base = base
    self.path = path
    self.headers = header
    self.downloader = SimpleDownloader(base, path, header)
    self.file_id = 1

  def get(self, url_or_soup, selector):
    if not isinstance(selector, SelectorCommand):
      raise Exception("selector must be <class 'SelectroCommand'>")

    if isinstance(url_or_soup, BeautifulSoup):
      soup = url_or_soup
    else:
      url = urllib.parse.urljoin(self.base, url_or_soup)
      response = requests.get(url, headers=self.headers)

      if not response.ok:
        raise Exception('html not 200 error')

      html = response.text
      soup = BeautifulSoup(html, 'html.parser')

    self.file_id += 1
    img_urls = map(lambda img : img[selector.attribute], soup.select(selector.element))

    for img_url in img_urls:
      yield self.downloader.get(img_url)

  def compress(self, url_or_soup, selector):
    responses = self.get(url_or_soup, selector)
    file = BytesIO()
    zf = ZipFile(file, 'w')
    for i, response in enumerate(responses, start=1):
      ext = guess_extension(response['content-type'])
      zf.writestr(f'{i}{ext}', response['content'])
      print(f'{i}{ext}')
    
    return file

  def download(self, url_or_soup, selector, compress=False):
    if compress:
      path = os.path.join(self.path, f'{self.file_id}.zip')
      if os.path.exists(path):
        pass
      file = self.compress(url_or_soup, selector)
      with open(path, 'wb') as f:
        f.write(file.getvalue())
        print(path)
    else:
      path = os.path.join(self.path, str(self.file_id))
      if not os.path.isdir(path):
        os.mkdir(path)
      responses = self.get(url_or_soup, selector)
      for i, response in enumerate(responses, start=1):
        ext = guess_extension(response['content-type'])
        with open(os.path.join(path, f'{i}{ext}'), 'wb') as f:
          f.write(response['content'])
          print(f'{i}{ext}')
      print(path)


class DownloadManager:

  def __init__(self, downloader):
    self.downloader = downloader
    if not isinstance(downloader, WebContentDownloader):
      raise Exception('downloader must be child of WebContentDownloader')
    self.file_id = 1

  def get_list(self, url_or_soup, selector, slice_obj=None):
    if not isinstance(selector, SelectorCommand):
      raise Exception("selector must be <class 'SelectroCommand'>")

    if isinstance(url_or_soup, BeautifulSoup):
      soup = url_or_soup
    else:
      url = urllib.parse.urljoin(self.downloader.base, url_or_soup)
      response = requests.get(url, headers=self.downloader.headers)

      if not response.ok:
        raise Exception('html not 200 error')

      html = response.text
      soup = BeautifulSoup(html, 'html.parser')

    self.file_id += 1
    if isinstance(slice_obj, slice):
      post_urls = map(lambda post : post[selector.attribute], soup.select(selector.element)[slice_obj])
    else:
      post_urls = map(lambda post : post[selector.attribute], soup.select(selector.element))

    for post_url in post_urls:
      yield post_url

  def download(self, url_or_soup, list_selector, img_selector, slice_obj=None, compress=False):
      urls = self.get_list(url_or_soup, list_selector, slice_obj)
      for url in urls:
        self.downloader.download(url, img_selector, compress)
  