from ezcliy import Command
from .sample import copy_sample


class PipenvAmigo(Command):
    class Update(Command):
        allow_empty_calls = True

        def invoke(self):
            copy_sample()
