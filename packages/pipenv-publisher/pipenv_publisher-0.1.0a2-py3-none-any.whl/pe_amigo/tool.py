from ezcliy import *
from pathlib import Path


class PipenvAmigo(Command):
    class Update(Command):
        package_name = Positional('package', ask_if_missing='package name')

        def invoke(self):
            package_dir = Path.cwd().joinpath(str(self.package_name))
