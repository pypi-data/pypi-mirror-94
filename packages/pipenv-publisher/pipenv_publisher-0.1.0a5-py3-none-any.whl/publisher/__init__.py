from publisher.tool import PipenvAmigo
from publisher._version import __version__, __author__

if __name__ == '__main__':
    PipenvAmigo().entry('setup')
else:
    def run():
        PipenvAmigo().cli_entry()
