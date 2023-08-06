from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ServerMaker',
  version='0.0.2',
  description='A server and client maker',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pikhunyk David',
  author_email='pikhunykdavid@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='server',
  packages=find_packages(),
  install_requires=[''] 
)