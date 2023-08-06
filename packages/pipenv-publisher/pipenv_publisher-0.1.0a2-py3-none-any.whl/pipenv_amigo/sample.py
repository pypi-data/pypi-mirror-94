from pathlib import Path
import shutil


sample_path = Path(__file__).parent.joinpath('_sample_setup.py')


def copy_sample():
    shutil.copyfile(sample_path, Path.cwd().joinpath('setup.py'))
