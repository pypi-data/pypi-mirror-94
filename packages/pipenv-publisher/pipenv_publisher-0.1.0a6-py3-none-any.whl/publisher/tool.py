from ezcliy import Command, Positional, Flag
from pipenv.project import Project

from .meta import create_meta_json, add_meta_json_pkg
from .sample import copy_sample_setup, add_sctipts, copy_version, create_setup_section
from .setup_json import generate_setup_json


class PipenvAmigo(Command):
    def invoke(self):  # Temp fix
        if len(self.values):
            print(self._helpman.render_help(self))

    class Setup(Command):
        name = 'setup'
        description = 'Creates setup.py'
        allow_empty_calls = True

        def invoke(self):
            # Pipfile changes
            create_setup_section()
            add_sctipts()
            # Copy files
            copy_sample_setup()
            # First run
            generate_setup_json()

    class VersionStamp(Command):
        name = 'stamp'
        description = 'Recreates meta.json and updates _version.py'
        pkg_name = Positional('package')
        pkg_name.description = 'Directory of package.'
        no_copy = Flag('--no-copy')
        no_copy.description = 'Passing this flag results in skipping copying of _version file.'
        restrict_to_positionals_only = True

        def invoke(self):
            if str(self.pkg_name) == '.':
                project = Project(which='Pipfile')
                self.pkg_name.value = str(project.parsed_pipfile['setup']['packages'][0])
                print(self.pkg_name.value)

            if not self.no_copy:
                copy_version(str(self.pkg_name))
                print('Remember to add import in __init__')

            add_meta_json_pkg(str(self.pkg_name))
            create_meta_json(str(self.pkg_name))

    class Lock(Command):
        allow_empty_calls = True

        def invoke(self):
            generate_setup_json()
