import click

import _utils_


@click.command()
def main():
    skip = 0
    limit = 40
    while True:
        projs = _utils_.httpGetWithCookies('ampm/project/fetch',
                                           params={
                                               'skip': skip,
                                               'limit': limit
                                           })

        for proj in projs:
            click.echo(f"{proj['name']}")

        l = len(projs)
        if l < limit:
            break
        else:
            skip += limit
