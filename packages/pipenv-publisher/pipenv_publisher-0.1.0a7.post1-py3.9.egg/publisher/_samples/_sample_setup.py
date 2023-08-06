import json
from pathlib import Path

from setuptools import setup


auto_detect = {}
pkg_path = Path(__file__).parent

# RST detection
if pkg_path.joinpath('README.rst').exists():
    with Path.cwd().joinpath('README.rst').open('r') as f:
        auto_detect = auto_detect | {'long_description': f.read()}

# Markdown detection
if pkg_path.joinpath('README.md').exists():
    with Path.cwd().joinpath('README.md').open('r') as f:
        auto_detect = auto_detect | {'long_description_content_type': "text/markdown", 'long_description': f.read()}

with pkg_path.joinpath('setup-lock.json').open('r') as f:
    setup_lock = json.load(f)

setup(
    **setup_lock,
    **auto_detect
)
exit()
# Fallback for pipenv local loading
setup(
    name=setup_lock['name'],
    version=setup_lock['version'],
    author=setup_lock['author'],
    packages=setup_lock['packages'],
    install_requires=setup_lock['install_requires'],
)
