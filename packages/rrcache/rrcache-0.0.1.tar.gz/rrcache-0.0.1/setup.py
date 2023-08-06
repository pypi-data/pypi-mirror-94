from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='rrcache',
  version='0.0.1',
  description='just a practice',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Turtle',
  author_email='satyam.krait@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='practice', 
  packages=find_packages(),
  install_requires=['redis'] 
)
