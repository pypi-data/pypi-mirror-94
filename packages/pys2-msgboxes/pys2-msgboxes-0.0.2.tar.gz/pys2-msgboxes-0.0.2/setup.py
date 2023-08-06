from setuptools import setup, find_packages
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

 
setup(
  name='pys2-msgboxes',
  version='0.0.2',
  description='Pre-built Messageboxes for PySide2 Applications',
  long_description_content_type='text/markdown',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/StrtCoding/pys2-msgboxes',  # the URL of your package's home page e.g. github link
  author='Straight Coding',
  author_email='strtcodingcontact@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='PySide2 QMessageBox pys2-msgboxes', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  include_package_data=True,
  install_requires=['PySide2>=5.15.0'] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)