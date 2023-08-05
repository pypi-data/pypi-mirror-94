from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='formatting',
  version='0.0.1',
  description='A formatting function',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jayant Gupta',
  author_email='jayantgupta036@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='formatting', 
  packages=find_packages(),
  install_requires=[''] 
)