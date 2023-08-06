import click
import re
import PyInquirer

import _utils_
import passwd


@click.command()
def main():
    signupPromptOpts = [
        {
            'type': 'input',
            'name': 'email',
            'message': 'What\'s your email',
            'validate': _utils_.validateEmail
        },
        {
            'type':
            'input',
            'name':
            'name',
            'message':
            'What\'s your name',
            'validate':
            lambda val: len(val) >= 6 or 'name length must be greater than 6'
        },
    ]
    signupPromptRep = PyInquirer.prompt(signupPromptOpts)
    _utils_.httpPost('ampm/signup', data=signupPromptRep)
    click.echo(f"Info: sent captcha to {signupPromptRep['email']}")

    passwd.setPassword(signupPromptRep['email'])
