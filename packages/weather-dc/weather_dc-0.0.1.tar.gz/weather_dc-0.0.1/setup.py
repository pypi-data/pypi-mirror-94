from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='weather_dc',
  version='0.0.1',
  description='Prints weather of Washington DC also creates a excel file of the forecast.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sai Shyam',
  author_email='sai.shyam0602@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='weather', 
  packages=find_packages(),
  install_requires=[''] 
)