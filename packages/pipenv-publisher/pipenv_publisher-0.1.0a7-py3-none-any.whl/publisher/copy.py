import shutil
from pathlib import Path


def copy_sample(name: str):
    shutil.copyfile(Path(__file__).parent.joinpath(f'_samples/_sample_{name}'), Path.cwd().joinpath(name))


def copy_shim(name: str):
    shutil.copyfile(Path(__file__).parent.joinpath(f'_samples/_shim_{name}'), Path.cwd().joinpath(name))
