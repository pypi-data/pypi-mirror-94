import click
import PyInquirer
import rsa
import re
import time
import base64

import _utils_


def setPassword(email):
    codeOpts = [{
        'type':
        'input',
        'name':
        'code',
        'message':
        'verification code',
        'validate':
        lambda val: len(val) == 5 or 'verification code length must be equal 5'
    }]
    codePromptRep = PyInquirer.prompt(codeOpts)

    passwdOpts = [{
        'type':
        'password',
        'message':
        'What\'s your password',
        'name':
        'password',
        'validate':
        lambda val: len(val) >= 6 or 'password length must be greater than 6'
    }, {
        'type': 'password',
        'message': 'Confirm your password',
        'name': 'cPassword'
    }]
    while True:
        passwdPromptRep = PyInquirer.prompt(passwdOpts)
        if passwdPromptRep['password'] == passwdPromptRep['cPassword']:
            break
        click.echo('Error: The two passwords are not the same')

    keystr = _utils_.httpGet('ampm/pubkey')
    pubkey = rsa.PublicKey.load_pkcs1(keystr.encode())
    password = passwdPromptRep['password']
    encode = rsa.encrypt(password.encode(), pubkey)

    bodyDict = {
        'email': email,
        'code': codePromptRep['code'],
        'password': base64.b64encode(encode).decode("utf-8")
    }

    _utils_.httpPost('ampm/passwd', data=bodyDict)

    click.echo('Info: set password success!!')


@click.command()
def main():
    emailPromptOpts = [{
        'type': 'input',
        'name': 'email',
        'message': 'What\'s your email',
        'validate': _utils_.validateEmail
    }]

    emailPromptRep = PyInquirer.prompt(emailPromptOpts)

    _utils_.httpPost('ampm/passwd-code', data=emailPromptRep)
    click.echo(f"Info: sent captcha to {emailPromptRep['email']}")
    setPassword(emailPromptRep['email'])
