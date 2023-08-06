import os
from setuptools import find_packages
from setuptools import setup


# First time install this library
# python setup.py bdist_wheel
# pip install dist/sk_ensembler-0.1.0-py3-none-any.whl


lib_folder = os.path.dirname(os.path.realpath(__file__))
requirements_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as fp:
        install_requires = fp.read().splitlines()


setup(
    name='nlp4ml',
    packages=find_packages(include=['nlp4ml']),
    version='0.1.0',
    description='Python NLP wrapper',
    author='Yang Wang',
    license='MIT',
    install_requires=install_requires,
    tests_require=['pytest==4.4.1'],
    setup_requires=['pytest-runner'],
    test_suite='tests'
)
