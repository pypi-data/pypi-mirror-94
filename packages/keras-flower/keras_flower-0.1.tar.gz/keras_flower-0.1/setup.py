from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='keras_flower',
      version='0.1',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='A Simple Flower classification package trained on DenseNet201',
      url='https://github.com/Bhanuchander210/keras_flower.git',
      author='Bhanuchander Udhayakumar',
      author_email='bhanuchander210@gmail.com',
      license='MIT',
      packages=['keras_flower'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['tensorflow>=2.2.0', 'keras>=2.4.3', 'pillow>=8.0.1']
      )
