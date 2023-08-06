from os import path
from sys import path as sysPath

here = path.abspath(path.dirname(__file__))
parent = path.dirname(here)
sysPath.append(parent)
sysPath.append(here)

import _utils_
import click

import init


@click.group()
def main():
    pass


@click.command()
def version():
    click.echo("xbimer-cli " + _utils_.VERSION)


main.add_command(version, "version")
main.add_command(init.main, "init")

if __name__ == "__main__":
    main()