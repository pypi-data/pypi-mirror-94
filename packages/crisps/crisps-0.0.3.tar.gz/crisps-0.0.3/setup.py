from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='crisps',
  version='0.0.3',
  description='Eat and get fat.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='IYEIds',
  author_email='yigidogulay@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='crisps, fat, chabby, eat', 
  packages=find_packages(),
  install_requires=[''] 
)
