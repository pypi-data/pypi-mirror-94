from setuptools import setup, find_packages
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='wallstreetbets-sentiment-analyser',
  version='0.0.1',
  description='A tool for extracting post from the wallstreetbets reddit group and running them through a sentiment analyser (vadar).',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/squeakycheese75/wallstreetbets-sentiment-analyser',  # the URL of your package's home page e.g. github link
  author='Jamie Wooltorton',
  author_email='james_wooltorton@hotmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='wallstreetbets reddit sentiment analyser', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=[''] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)