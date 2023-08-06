import json
from pathlib import Path

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip


def generate_setup_json():
    project = Project(which='Pipfile')
    print('Locking setup section from Pipfile...')
    setup_dict = project.parsed_pipfile['setup'].copy()
    print('Locking declared dependencies...')
    setup_dict['install_requires'] = convert_deps_to_pip(
        project.packages, project=project, r=False, include_index=False
    )
    print('Saving lock...')
    with Path.cwd().joinpath('setup-lock.json').open('w') as f:
        json.dump(setup_dict, f, indent=2)
    print(f'Done. Locked {len(setup_dict)} values!')
