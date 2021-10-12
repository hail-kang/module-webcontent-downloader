import abc

class WebContentDownloader(metaclass=abc.ABCMeta):
  """
  다운로더 클래스들의 인터페이스
  """

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

class SelectorDonwloader(WebContentDownloader, metaclass=abc.ABCMeta):
  """
  선택자를 사용한 다운로더들의 인터페이스
  한 페이지 안의 여러장의 이미지를 다운로드 함
  """
  pass