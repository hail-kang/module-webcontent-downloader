import os
import urllib.parse
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
from mimetypes import guess_extension

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from .interface import SelectorDonwloader
from .simpledownloader import SimpleDownloader
from .utils import SelectorCommand

class RequestsDownloader(SelectorDonwloader):
  """
  requests 모듈을 사용하여 HTML을 얻어내는 다운로더
  """

  def __init__(self, base, path, 
    headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    """
    :Args:
     - base - 다운로드 할 링크의 host를 적는다. 만약 다운로드할 url의 입력값이 상대 경로로 주어져도 처리할 수 있도록 돕는다.
     - path - 다운로드 할 로컬 경로를 적는다.
     - headers - headers
    """
    self.base = base
    self.path = path
    self.headers = headers
    self.downloader = SimpleDownloader(base, path, headers)

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

  def download(self, url_or_soup, selector, name, compress=False):
    if compress:
      path = os.path.join(self.path, f'{name}.zip')
      if os.path.exists(path):
        pass
      file = self.compress(url_or_soup, selector)
      with open(path, 'wb') as f:
        f.write(file.getvalue())
        print(path)
    else:
      path = os.path.join(self.path, str(name))
      if not os.path.isdir(path):
        os.mkdir(path)
      responses = self.get(url_or_soup, selector)
      for i, response in enumerate(responses, start=1):
        ext = guess_extension(response['content-type'])
        with open(os.path.join(path, f'{i}{ext}'), 'wb') as f:
          f.write(response['content'])
          print(f'{i}{ext}')
      print(path)

class SeleniumDownloader(SelectorDonwloader):
  """
  selenium 모듈을 사용한 다운로더
  """

  def __init__(self, base, path, driver,
    headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    }):
    """
    :Args:
     - base - 다운로드 할 링크의 host를 적는다. 만약 다운로드할 url의 입력값이 상대 경로로 주어져도 처리할 수 있도록 돕는다.
     - path - 다운로드 할 로컬 경로를 적는다.
     - driver - Chrome 드라이버를 사용해야하며, Webdriver 인스턴스 또는 Chromedriver가 위치한 경로를 받는다.
     - headers - headers
    """
    self.base = base
    self.path = path
    if isinstance(driver, webdriver.Chrome):
      self.driver = driver
    elif isinstance(driver, str):
      options = webdriver.ChromeOptions()
      options.add_argument('headless')
      options.add_argument('window-size=1920x1080')
      options.add_argument("--lang=ko-KR")
      options.add_argument("disable-gpu")
      self.driver = webdriver.Chrome(driver, options=options)
    else:
      raise Exception('driver must be webdriver_object or driver_location')
    self.headers = headers
    self.downloader = SimpleDownloader(base, path, headers)

  def get(self, url_or_soup, selector):
    if not isinstance(selector, SelectorCommand):
      raise Exception("selector must be <class 'SelectroCommand'>")

    if isinstance(url_or_soup, BeautifulSoup):
      soup = url_or_soup
    else:
      url = urllib.parse.urljoin(self.base, url_or_soup)
      self.driver.get(url)
      html = self.driver.page_source
      soup = BeautifulSoup(html, 'html.parser')

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

  def download(self, url_or_soup, selector, name, compress=False):
    if compress:
      path = os.path.join(self.path, f'{name}.zip')
      if os.path.exists(path):
        pass
      file = self.compress(url_or_soup, selector)
      with open(path, 'wb') as f:
        f.write(file.getvalue())
        print(path)
    else:
      path = os.path.join(self.path, str(name))
      if not os.path.isdir(path):
        os.mkdir(path)
      responses = self.get(url_or_soup, selector)
      for i, response in enumerate(responses, start=1):
        ext = guess_extension(response['content-type'])
        with open(os.path.join(path, f'{i}{ext}'), 'wb') as f:
          f.write(response['content'])
          print(f'{i}{ext}')
      print(path)