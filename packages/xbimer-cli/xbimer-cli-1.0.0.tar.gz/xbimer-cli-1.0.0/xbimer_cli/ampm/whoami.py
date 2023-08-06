import click

import _utils_


@click.command()
def main():
    info = _utils_.httpGetWithCookies('ampm/whoami')
    click.echo(f"{info['name']} <{info['email']}>")
