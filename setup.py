#!/usr/bin/env python3

from setuptools import setup

setup(name='Scheduler',
        version='1.0',
        description='TVision Device Scheduler',
        author='Mark Buckaway',
        author_email='mark@buckaway.ca',
        url='https://github.com/tvision',
        include_package_data=True,
        packages=['configlib'],
        entry_points = {'console_scripts': [
            'scheduler = configlib.cli_scheduler:main', 
            ]},
        install_requires=[
            'pyyaml',
            'zc.lockfile',
            'wheel',
            'zc.lockfile',
            'psutil'
        ]
)