from pipenv_amigo.tool import PipenvAmigo


if __name__ == '__main__':
    PipenvAmigo().entry('update', 'pe_amigo')
else:
    def run():
        PipenvAmigo().cli_entry()
