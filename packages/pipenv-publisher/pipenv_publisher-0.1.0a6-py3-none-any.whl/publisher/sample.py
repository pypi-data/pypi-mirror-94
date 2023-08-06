from pathlib import Path
import shutil

from pipenv.project import Project


def copy_sample_setup():
    print('Copy setup.py')
    shutil.copyfile(Path(__file__).parent.joinpath('_sample/_sample_setup.py'), Path.cwd().joinpath('setup.py'))


def copy_version(package_name: str):
    print('Copy _version.py')
    shutil.copyfile(Path(__file__).parent.joinpath('_sample/_sample_version.py'), Path.cwd().joinpath(package_name, '_version.py'))


def create_setup_section():
    keys_to_populate = ('name', 'mypkg'), ('version', '0.0.1'), ('author', 'me')
    project = Project(which='Pipfile')
    setup_section = project.parsed_pipfile.get('setup', {})

    for k, v in keys_to_populate:
        if k not in setup_section:
            print(f'Missing {k}! Temporarly set to {v}')
            setup_section.update({k: v})

    project.parsed_pipfile['setup'] = setup_section
    project.write_toml(project.parsed_pipfile)


def add_sctipts():
    project = Project(which='Pipfile')
    print('Adding wheel package to dev packages...')
    project.add_package_to_pipfile('wheel', dev=True)
    print('Adding scripts to Pipfile...')
    p = project.parsed_pipfile
    # noinspection PyTypeChecker
    p['scripts'] = p.get('scripts', {}) | {
        'build': 'python setup.py bdist_wheel build',
        'pub': 'pipenv-pub',
    }
    project.write_toml(p)
    print('Remember to lock Pipfile!')
