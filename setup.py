#!/usr/bin/env python3
from setuptools import setup

setup(
    name="kuwtg",
    version="0.0.1",
    packages=['kuwtg',
              'kuwtg.api',
              'kuwtg.api.consumer',
              'kuwtg.cmd',
              'kuwtg.obj',
              'kuwtg.ui',],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['kuwtg=kuwtg.cmd.console:main'],
    }
)
