import click
import re
import PyInquirer
import base64
import rsa

import _utils_


@click.command()
def main():
    signinPromptOpts = [
        {
            'type': 'input',
            'name': 'email',
            'message': 'What\'s your email',
            'validate': _utils_.validateEmail
        },
        {
            'type':
            'password',
            'message':
            'What\'s your password',
            'name':
            'password',
            'validate':
            lambda val: len(val) >= 6 or
            'password length must be greater than 6'
        },
    ]
    signipPromptRep = PyInquirer.prompt(signinPromptOpts)

    keystr = _utils_.httpGet('ampm/pubkey')
    pubkey = rsa.PublicKey.load_pkcs1(keystr.encode())
    password = signipPromptRep['password']
    encode = rsa.encrypt(password.encode(), pubkey)

    bodyDict = {
        'email': signipPromptRep['email'],
        'password': base64.b64encode(encode).decode("utf-8")
    }

    res = _utils_.httpPost('ampm/signin', data=bodyDict)
    _utils_.saveToken(res)
    click.echo('xbimer logined!!')
