from setuptools import setup
import os

setup(
        name=os.environ['DA_PYPI_PACKAGE'],
        version='0.0.2',
        description='',
        long_description='',
        packages=[],
        author='deepalign',
        install_requires=['deepalign-never-satisfied>10.0']
)
