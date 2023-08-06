# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:20:21 2021

@author: babe8901
"""

from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education Purpose for Students',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License'
    'Programming Language :: Python :: 3'
    ]

setup(
      name = 'babe8901',
      version = '0.0.1',
      description = '''This is a package for a calculator. It's provides you with the basic functionality of any calculator.
created by Shubham Yadav
on 09/02/2020''',
      Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
      url = '',
      author = 'Shubham Yadav',
      author_email = 'luckyshubham16@gmail.com',
      license = 'MIT',
      classifiers = classifiers,
      keywords = ['add','sub','mul','div'],
      packages = find_packages(),
      install_require = ['']
      )