from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Fuzzy Math',
  version='0.0.1',
  description='Performs Fuzzy Math Functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Nicholas R Furth',
  author_email='nf77@njit.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='Fuzzy Math', 
  packages=find_packages(),
  install_requires=[''] 
)