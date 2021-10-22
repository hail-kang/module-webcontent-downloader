
import urllib.parse
from threading import Thread

import requests
from bs4 import BeautifulSoup

from .interface import SelectorDonwloader
from .simpledownloader import SimpleDownloader
from .utils import SelectorCommand

class DownloadManager:
  """
  다운로더를 사용하여 다운로드 리스트를 각각 저장할 수 있도록 돕는 매니저 클래스
  """

  def __init__(self, downloader):
    self.downloader = downloader
    if not isinstance(downloader, SelectorDonwloader):
      raise Exception('downloader must be child of SelectorDonwloader')
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

    if isinstance(slice_obj, slice):
      post_urls = map(lambda post : post[selector.attribute], soup.select(selector.element)[slice_obj])
    else:
      post_urls = map(lambda post : post[selector.attribute], soup.select(selector.element))

    for post_url in post_urls:
      yield post_url

  def download(self, url_or_soup, list_selector, img_selector, slice_obj=None, compress=False, use_thread=False):
      urls = self.get_list(url_or_soup, list_selector, slice_obj)
      for url in urls:
        if use_thread:
          Thread(target=self.downloader.download, args=(url, img_selector, self.file_id, compress)).start()
        else:
          self.downloader.download(url, img_selector, self.file_id, compress)
        self.file_id += 1