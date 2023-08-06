#!/usr/bin/env python
 
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

import apkpatcher
 

setup(
    name='apkpatcher',
    version='0.0.7a',
    packages=['apkpatcher'],
    author="MadSquirrel",
    author_email="benoit.forgette@ci-yow.com",
    description="Decompile APK to Java",
    package_data={'apkpatcher': ['network_security_config.xml',
                                 'network_security_config_custom.xml',
                               'pyaml/libaml/android-attrs.json']},
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    download_url="https://gitlab.com/MadSquirrels/mobile/apkpatcher",
    include_package_data=True,
    url='https://ci-yow.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning"
    ],
 
    entry_points = {
        'console_scripts': [
            'apkpatcher=apkpatcher:main',
        ],
    },
    cmdclass={
    },
    install_requires = [
        'sty',
    ],
    python_requires='>=3.5'
 
)
