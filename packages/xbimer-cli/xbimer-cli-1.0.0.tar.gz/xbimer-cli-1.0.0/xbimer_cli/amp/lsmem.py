import click

import _utils_


@click.command()
def main():
    skip = 0
    limit = 40

    manifest = _utils_.readManifest()

    while True:
        mems = _utils_.httpGetWithCookies('amp/member/fetch',
                                          params={
                                              'skip': skip,
                                              'limit': limit,
                                              'id': manifest['id']
                                          })

        for mem in mems:
            click.echo(
                f"{mem['email']} <{mem['name']}> {'owner' if mem['isOwner'] == True else ''}"
            )

        l = len(mems)
        if l < limit:
            break
        else:
            skip += limit