from setuptools import setup

setup(
  name='webcontentdownloader',
  version='1.0.1',
  packages=['webcontentdownloader'],
  install_requires=[
    'requests >= 2.26',
    'beautifulsoup4 >= 4.10',
    'selenium >= 3.141',
  ]
)