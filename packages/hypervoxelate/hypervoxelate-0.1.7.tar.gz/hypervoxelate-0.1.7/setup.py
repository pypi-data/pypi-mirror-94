from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='hypervoxelate',
      long_description=long_description,
      version='0.1.7',
      description='Simple hypervoxelation procedure w/ support for jagged cut-points',
      url='http://github.com/califynic/hypervoxelate',
      author='Ali Cy',
      author_email='califynic@gmail.com',
      license='MIT',
      packages=['hypervoxelate'],
      zip_safe=False)
