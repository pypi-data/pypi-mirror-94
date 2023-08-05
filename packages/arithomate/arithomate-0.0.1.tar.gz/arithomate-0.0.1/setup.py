from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
readme = "This module helps to do Arithemetic Operations easily."
CHANGELOG = """Change Log
==========

0.0.1 (04/02/2021)
-------------------
- First Release"""
setup(
  name='arithomate',
  version='0.0.1',
  description='This module helps to do Arithemetic Operations easily.',
  long_description=readme + '\n\n' + CHANGELOG,
  url='',  
  author='Sai Santosh Pal',
  author_email='saisantoshpal@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='operators', 
  packages=find_packages(),
  install_requires=[''] 
)