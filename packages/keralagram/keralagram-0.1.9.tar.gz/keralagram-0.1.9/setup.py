# Keralagram - Telegram Bot Api Library Python
# Copyright (C) 2021  Anandpskerala <anandpskerala@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import re

from setuptools import setup, find_packages
from io import open


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("keralagram/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


setup(
    name="keralagram",
    version=version,
    description='Asynchronous Python API for building Telegram bots',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/KeralaBots/Keralagram",
    author='Anand P S',
    author_email='anandpskerala@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],
    keywords="telegram asyncio bot",
    project_urls={
        "Community": "https://t.me/KeralasBots",
        "Source": "https://github.com/KeralasBots/Keralagram",
    },
    packages=find_packages(exclude=["tests*"]),
    install_requires=requires
)
