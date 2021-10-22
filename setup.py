from setuptools import setup

setup(
  name='webcontentdownloader',
  version='2.0.0',
  packages=['webcontentdownloader'],
  install_requires=[
    'requests >= 2.26',
    'beautifulsoup4 >= 4.10',
    'selenium >= 3.141',
  ]
)