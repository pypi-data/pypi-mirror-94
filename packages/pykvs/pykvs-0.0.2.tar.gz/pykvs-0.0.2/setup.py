import os

from setuptools import setup, find_packages


def get_long_description():
    readme_filepath = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_filepath) as f:
        return f.read()


def get_version():
    version_filepath = os.path.join(os.path.dirname(__file__), 'pykvs', 'version.py')
    with open(version_filepath) as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split()[-1][1:-1]


def get_tests_requires():
    requirements_filepath = os.path.join(os.path.dirname(__file__), 'requirements-dev.txt')
    with open(requirements_filepath, 'r') as f:
        return f.read().splitlines()


setup(
    name='pykvs',
    version=get_version(),
    url='https://github.com/yutayamazaki/pykvs',
    author='Yuta Yamazaki',
    author_email='yu.yamazakii@gmail.com',
    maintainer='Yuta Yamazaki',
    maintainer_email='yu.yamazakii@gmail.com',
    description='Python simple key-value store.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    license='MIT',
    keywords='python',
)
