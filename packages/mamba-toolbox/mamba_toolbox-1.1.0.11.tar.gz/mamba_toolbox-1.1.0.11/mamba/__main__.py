import click
from .commands import new_project, build_package

@click.group()
def cli():
    pass

cli.add_command(new_project)
cli.add_command(build_package)



if __name__ == "__main__":
    cli()
