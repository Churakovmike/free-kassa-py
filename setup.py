import io
import os
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        description = '\n'+ f.read()
except FileNotFoundError:
    description = 'long_description'

setup(
    name='free-kassa-py',
    version='1.0.1',
    description='FreeKassa python 3 client',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/Churakovmike/free-kassa-py',
    author='Mikhail Churakov',
    author_email='churakovmike@mail.ru',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='freekassa',

    packages=find_packages(exclude=['tests']),

    install_requires=['requests'],

    python_requires='>3.4',

    project_urls={
        'Source': 'https://github.com/Churakovmike/free-kassa-py'
    }
)
