import click
import PyInquirer

import _utils_


@click.command()
def main():
    manifest = _utils_.readManifest()

    rmmemPromptOpts = [{
        'type': 'input',
        'name': 'email',
        'message': 'What\'s the member email',
        'validate': _utils_.validateEmail
    }]
    rmmemPromptRep = PyInquirer.prompt(rmmemPromptOpts)

    _utils_.httpPostWithCookies('amp/member/remove',
                                data={
                                    'id': manifest['id'],
                                    'member': rmmemPromptRep['email']
                                })

    click.echo('successfully!!')