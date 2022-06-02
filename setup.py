from setuptools import find_packages, setup

setup(
    name='BooleanAI',
    packages=find_packages(include=['booleanai']),
    version='1.0.0',
    description='A different approch to create an AI',
    author='Gooxey',
    license='MIT',
    install_requires=['datetime', 'bitarray']
)