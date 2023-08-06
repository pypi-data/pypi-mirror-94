import click
import PyInquirer

import _utils_


@click.command()
def main():
    manifest = _utils_.readManifest()

    admemPromptOpts = [{
        'type': 'input',
        'name': 'email',
        'message': 'What\'s the member email',
        'validate': _utils_.validateEmail
    }]
    admemPromptRep = PyInquirer.prompt(admemPromptOpts)

    _utils_.httpPostWithCookies('amp/member/addition',
                                data={
                                    'id': manifest['id'],
                                    'member': admemPromptRep['email']
                                })

    click.echo('successfully!!')