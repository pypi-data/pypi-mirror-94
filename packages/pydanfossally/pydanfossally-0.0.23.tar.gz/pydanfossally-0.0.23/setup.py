# -*- coding: utf-8 -*-

from pydanfossally import __version__
import setuptools

requirements = []

setuptools.setup(
    name = 'pydanfossally',
    version = __version__,
    description = 'Danfoss Ally API library',
    author = 'Morten Trab',
    author_email = 'morten@trab.dk',
    license= 'MIT',
    url = 'https://github.com/mtrab/pydanfossally',
    packages=setuptools.find_packages(),
    install_requires=requirements,
)