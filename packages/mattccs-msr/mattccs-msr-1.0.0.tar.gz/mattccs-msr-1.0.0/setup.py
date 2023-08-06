"""
PyPI setup file
"""

from setuptools import setup


setup(
    name = 'mattccs-msr',
    packages = ['msr'],
    version = '1.0.0',
    author='Matt Cotton',
    author_email='matthewcotton.cs@gmail.com',
    url='https://github.com/MattCCS/mattccs-msr',

    description='Sym 2021 Coding Challenge',
    long_description=open("README.md").read(),
    classifiers=["Programming Language :: Python :: 3"],

    entry_points={
        'console_scripts': [
            'msr=msr.main:main',
        ],
    },

    install_requires=[
        'validators',
        'requests',
        'tabulate',
        'tldextract',
    ],
)
