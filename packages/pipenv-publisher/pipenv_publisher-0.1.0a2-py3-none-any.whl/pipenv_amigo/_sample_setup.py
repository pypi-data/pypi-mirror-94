# noinspection DuplicatedCode
from pathlib import Path

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import setup

project = Project(which='Pipfile')

auto_detect = {}

if Path.cwd().joinpath('README.md').exists():
    with Path.cwd().joinpath('README.md').open('r') as f:
        auto_detect = auto_detect | {'long_description_content_type': "text/markdown", 'long_description': f.read()}

setup(
    install_requires=convert_deps_to_pip(
        project.packages, project=project, r=False, include_index=False
    ),
    **project.parsed_pipfile['setup'],
    **auto_detect
)
