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
  셀렉터를 사용한 다운로더들의 인터페이스
  """
  pass