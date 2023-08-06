from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().split('\n')

install_requires = [x.strip() for x in requirements if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in requirements \
                    if 'git+' not in x]

setup(
        name = "Phinder",
        version = "0.0.3",
        descriptoin = "Semi-Automated Pharmacophore Generation using Fragment Docking in GNINA",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/gnina/phinder",
        author="Dillon Gavlock & Samuel Cho",
        author_email="dcg33@pitt.edu",
            license="MIT",
        classifiers=(
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ),
        packages= find_packages(),
        entry_points = {
            'console_scripts': [
                "Phinder = cli:main",
                "dock = Phinder.docking.docker:main"
                "phind = Phinder.PharmacoFindWorkplace.POpt2:main"
                ]
            },
        install_requires = requirements
        )
