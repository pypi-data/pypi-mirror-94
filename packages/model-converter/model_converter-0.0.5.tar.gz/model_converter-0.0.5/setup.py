# coding=utf8
__author__ = 'liming'

from setuptools import setup

setup(name='model_converter',
      version='0.0.5',
      description='Convert Pydantic Model to Dart Class',
      url='https://github.com/ipconfiger',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='MIT',
      packages=['model_converter'],
      install_requires=[],
      entry_points={
          'console_scripts': ['covertmd=model_converter.main:main'],
      },
      zip_safe=False)
