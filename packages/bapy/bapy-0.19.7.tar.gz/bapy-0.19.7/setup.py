#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import find_packages
from setuptools import setup

from bapy import package
from bapy import Url
from bapy import User
# from bapy import ic
# ic(package.path)
# ic(package.project.description())
# ic(package.project)
# ic(package.project.requirements)
# ic(package.project.scripts_relative)
# ic(package.project.scripts)

setup(
    author=User.gecos,
    author_email=Url.email(),
    description=package.project.description(),
    entry_points={
        'console_scripts': [
            f'{package.repo} = {package.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=package.project.requirements['requirements'],
    name=package.repo,
    package_data={
        package.repo: [f'{package.repo}/scripts/*', f'{package.repo}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.9,<4',
    scripts=package.project.scripts_relative,
    setup_requires=package.project.requirements['requirements_setup'],
    tests_require=package.project.requirements['requirements_test'],
    url=Url.lumenbiomics(http=True, repo=package.repo).url,
    use_scm_version=False,
    version='0.19.7',
    zip_safe=False,
)
