# module-webcontent-downloader
웹 상의 이미지를 쉽게 다운로드 할 수 있도록 도와주는 모듈

# 필요 모듈
- requests >= 2.26
- beautifulsoup4 >= 4.10
- selenium >= 3.141

# 해당 모듈 설치
```
pip install webcontentdownloader
```

# 사용 방법
- 웹툰을 다운로드 하는 경우로 예시
```python
# RequestsDownloader 사용

from webcontentdownloader import *

downloader = RequestsDownloader(
  'https://comic.naver.com/', 
  r'C:\Users\Kang\Downloads\호랑이형님', 
)

selector = SelectorCommand('.wt_viewer img', 'src')
downloader.download('/webtoon/detail?titleId=650305&no=332&weekday=sat', selector)
```
- SeleniumDownloader를 사용한다면 chromedirver를 미리 준비해야 한다.
```python
# SeleniumDownloader 사용

from webcontentdownloader import *

downloader = SeleniumDownloader(
  'https://comic.naver.com/', 
  r'C:\Users\Kang\Downloads\호랑이형님', 
  r'C:\Users\Kang\Downloads\chromedriver_win32\chromedriver.exe'
)

selector = SelectorCommand('.wt_viewer img', 'src')
# compress=True를 사용하여 압축기능 사용
downloader.download('/webtoon/detail?titleId=650305&no=332&weekday=sat', selector, True)
```
- DownloadManager를 사용하여 여러 목록의 이미지 다운로드 가능
```python
# DownloadManager 사용

from webcontentdownloader import *

downloader = RequestsDownloader(
  'https://comic.naver.com/', 
  r'C:\Users\Kang\Downloads\호랑이형님', 
)

list_selector = SelectorCommand('.viewList tr:not(.band_banner) td.title a', 'href')
img_selector = SelectorCommand('.wt_viewer img', 'src')

manager = DownloadManager(downloader)
manager.download('/webtoon/list?titleId=650305&weekday=sat', list_selector, img_selector)
```
