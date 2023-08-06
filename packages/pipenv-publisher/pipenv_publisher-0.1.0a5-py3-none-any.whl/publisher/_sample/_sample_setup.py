import json
from pathlib import Path

from setuptools import setup


auto_detect = {}

# RST detection
if Path.cwd().joinpath('README.rst').exists():
    with Path.cwd().joinpath('README.rst').open('r') as f:
        auto_detect = auto_detect | {'long_description': f.read()}

# Markdown detection
if Path.cwd().joinpath('README.md').exists():
    with Path.cwd().joinpath('README.md').open('r') as f:
        auto_detect = auto_detect | {'long_description_content_type': "text/markdown", 'long_description': f.read()}

with Path.cwd().joinpath('setup-lock.json').open('r') as f:
    setup_lock = json.load(f)

setup(
    **setup_lock,
    **auto_detect
)
