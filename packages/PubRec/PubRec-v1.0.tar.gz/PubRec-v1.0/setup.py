#!/usr/bin/env python

from distutils.core import setup

setup(
  name = 'PubRec',
  version = 'v1.0',      
  license ='MIT',  
  description = 'Simple python module to get the number of citations of a paper (or list of papers)',
  long_description='See the github `repository <https://github.com/GiacobboNicola/PubRec>`_.',
  long_description_content_type="text/markdown",
  author = 'Nicola Giacobbo',
  author_email = 'giacobbo.nicola@gmail.com', 
  url = 'https://github.com/GiacobboNicola/PubRec',   
  download_url = 'https://github.com/GiacobboNicola/PubRec/archive/v1.0.tar.gz', 
  keywords = ['ADS', 'citations'],
  py_modules = ['pubrec'],
  scripts = ['bin/pubrec'],
  #packages=setuptools.find_packages(),
  install_requires=[        
          'bs4',
          'tqdm',
      ],
  include_package_data=True,
  classifiers = [
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
