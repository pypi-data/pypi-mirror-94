from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from pipenv.vendor import toml

from publisher.utils import downgrade_dict


class PyProjectManager:
    def __init__(self, filename='pyproject.toml'):
        self.__filename = filename
        with open(self.__filename, 'r') as f:
            self._content: dict = toml.load(f)

    def update_contents(self):
        with open(self.__filename, 'w') as f:
            toml.dump(self._content, f)
        print('Updated pyproject')

    def get_pipfile_deps(self, pipfile=Project(which='Pipfile')):
        self._content.update(
            {
                'project': {
                    'dependencies': convert_deps_to_pip(pipfile.packages, pipfile, r=False, include_index=False),
                    **downgrade_dict(pipfile.parsed_pipfile.get('project', {}))
                }
            }
        )
        self.update_contents()
