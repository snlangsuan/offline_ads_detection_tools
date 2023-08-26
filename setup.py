from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
  long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as fh:
  requirements = fh.read()

setup(
  name= 'offline-ads-detection-tools',
  version= '0.0.1',
  author= 'decimo.me',
  license= 'MIT',
  description= 'Util tools for project Offline Ads Detection',
  long_description= long_description,
  long_description_content_type= 'text/markdown',
  py_modules= ['offline_ads_detection_tools', 'app'],
  packages= find_packages(),
  install_requires= [requirements],
  python_requires= '>=3.8',
  classifiers= [
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  entry_points = '''
    [console_scripts]
    offline_ads_detection_tools=offline_ads_detection_tools:cli
  '''
)