import json

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

project = Project(which='Pipfile')


def something():
    with open('setup.json', 'w') as file:
        setup_dict = project.parsed_pipfile['setup']
        setup_dict['install_requires'] = convert_deps_to_pip(project.packages, project=project, r=False, include_index=False)
        json.dump(setup_dict, file, indent=2)


if __name__ == '__main__':
    something()
