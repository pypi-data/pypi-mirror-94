from setuptools import setup, find_packages

setup(
    name='scriptify',
    version='0.0.1',
    packages=find_packages(),
    description='turns functions into command line scripts',
    python_requires='>=3.6',
    author='Klas Leino',
    long_description='file: README.md',
    long_description_content_type='text/markdown')
