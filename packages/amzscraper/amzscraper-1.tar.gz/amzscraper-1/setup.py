from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='amzscraper',
  version='1',
  description='Some very basic codes with very limited uses. AMZ EXTRACTER',
  long_description=open('CHANGELOG.txt').read(),
  url='',  
  author='ROHIT_PRO_04',
  author_email='proboy440@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='SCRAPER', 
  packages=find_packages(),
  install_requires=[''] 
)