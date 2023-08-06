from os import path
from sys import path as sysPath

here = path.abspath(path.dirname(__file__))
parent = path.dirname(here)
sysPath.append(parent)
sysPath.append(here)

import _utils_
import signin
import passwd
import signup
import whoami
import lsproj

import click


@click.group()
def main():
    pass


@click.command()
def version():
    click.echo("xbimer-cli " + _utils_.VERSION)


main.add_command(signup.main, "signup")
main.add_command(passwd.main, "passwd")
main.add_command(signin.main, "signin")
main.add_command(whoami.main, "whoami")
main.add_command(version, "version")
main.add_command(lsproj.main, "lsproj")

if __name__ == "__main__":
    main()
