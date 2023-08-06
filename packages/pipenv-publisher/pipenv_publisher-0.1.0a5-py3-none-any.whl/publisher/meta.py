import json
from pathlib import Path

from pipenv.project import Project


def create_meta_json(package_name: str):
    project = Project(which='Pipfile')
    setup_dict = project.parsed_pipfile['setup'].copy()
    print('Saving author and version...')
    meta_dict = {'a': setup_dict['author'], 'v': setup_dict['version']}
    with Path.cwd().joinpath(package_name, 'meta.json').open('w') as f:
        json.dump(meta_dict, f, ensure_ascii=False)
    print(f'Saved meta.json for {package_name}!')


def add_meta_json_pkg(package_name: str):
    project = Project(which='Pipfile')
    setup_dict = project.parsed_pipfile['setup']
    print('Adding meta.json into setup')
    setup_dict.update({'package_data': {
        package_name: [
            'meta.json'
        ]
    }})
    project.write_toml(project.parsed_pipfile | {'setup': setup_dict})
