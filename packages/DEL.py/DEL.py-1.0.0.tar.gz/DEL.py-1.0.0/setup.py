from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name = 'DEL.py',
  packages=['delpy'],
  version = '1.0.0',
  license='MIT',
  description = 'API wrapper for discordextremelist',
  author = 'Moksej',
  author_email = 'moksej@gmail.com',
  url = 'https://github.com/discordextremelist/del.py',
  download_url = 'https://github.com/discordextremelist/del.py.git',
  install_requires=['aiohttp'],
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)