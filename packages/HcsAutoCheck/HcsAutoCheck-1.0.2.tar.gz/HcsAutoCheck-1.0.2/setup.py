# -*- coding: utf-8 -*- 
from setuptools import setup

setup(
    name = 'HcsAutoCheck',
    packages = ['HcsAutoCheck'],
    version = '1.0.2',
    license = 'MIT',
    description = '파이썬 교육청 자가진단 자동화',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author = 'Beta5051',
    author_email = 'beta5051@gmail.com',
    url = 'https://github.com/Beta5051/HcsAutoCheck',
    download_url='https://github.com/Beta5051/HcsAutoCheck/archive/master.tar.gz',
    keywords = ['covid', 'self-check', 'hcs'],
    install_requires = [
        'pycryptodome>=3.9.9',
        'requests>=2.25.1',
    ],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)