import setuptools
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='confluent_kafka_producers_wrapper',
    version='0.0.3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['avro-python3','requests', 'confluent-kafka'],
    url='https://github.com/antoniodimariano/confluent_kafka_producers_wrapper',
    license='',
    include_package_data=True,
    python_requires='~=3.7',
    author='Antonio Di Mariano',
    author_email='antonio.dimariano@gmail.com',
    description='Wrapper for producing messages using the confluent-kafka package.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
