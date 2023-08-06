import json
import warnings

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip


project = Project(which='Pipfile')


def conf_checks():
    required = 'version', 'name'
    for rk in required:
        if rk not in project.parsed_pipfile['setup']:
            warnings.warn('No key %s in Pipfile setup section!')


def create_setup_json():
    conf_checks()
    with open('setup.json', 'w') as file:
        setup_dict = project.parsed_pipfile['setup']
        setup_dict['install_requires'] = convert_deps_to_pip(
            project.packages, project=project, r=False, include_index=False
        )
        json.dump(setup_dict, file, indent=2)
