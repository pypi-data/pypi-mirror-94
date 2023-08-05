#!/usr/bin/env python

from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

#requires = open(file_requirements).read().strip().split('\n')
    
# This setup is suitable for "python setup.py develop".

setup(name='vre_eoles',
      version='0.1.4',
      description='toolbox for computing charge factor used in EOLES model',
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data = True,
      license = 'MIT',
      classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research'
        ],
      keywords = 'Image, data processing',
      install_requires = ['pandas',
                          'numpy',
                          'scipy',
                          'matplotlib',
                          'sklearn',
                          'adjustText'],
      author= 'ArrayStream(François Bertin)',
      author_email= 'francois.bertin7@wanadoo.fr',
      url= 'https://github.com/Bertin-fap/CIRED-ENS',
      packages=find_packages(),
      )
