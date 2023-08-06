from ezcliy import Command, Positional, Flag

from .meta import create_meta_json, add_meta_json_pkg
from .sample import copy_sample_setup, add_sctipts, copy_version, create_setup_section
from .setup_json import generate_setup_json


class PipenvAmigo(Command):
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
        pkg_name = Positional('package', ask_if_missing='name of package')
        pkg_name.description = 'Directory of package.'
        no_copy = Flag('--no-copy')
        no_copy.description = 'Passing this flag results in skipping copying of _version file.'

        def invoke(self):
            if not self.no_copy:
                copy_version(str(self.pkg_name))
                print('Remember to add import in __init__')
            add_meta_json_pkg(str(self.pkg_name))
            create_meta_json(str(self.pkg_name))

    class Lock(Command):
        allow_empty_calls = True

        def invoke(self):
            generate_setup_json()
