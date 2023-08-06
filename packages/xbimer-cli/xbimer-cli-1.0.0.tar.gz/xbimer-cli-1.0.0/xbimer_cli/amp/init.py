import click
import os
import PyInquirer
import json
import requests

import _utils_

from os import path


def nameValidate(val):
    l = len(val)

    if l < 4:
        return 'name length must be greater than 4'

    if l > 16:
        return 'The name length must be less than 16'

    return True


def archicadsValidate(vals):
    l = len(vals)
    if l == 0:
        return 'You must choose at least one topping.'

    return True


@click.command()
def main():
    xurl = 'https://api.github.com/repos/xbimer/xbimer/releases/latest'
    runtime = requests.get(xurl, timeout=10).json()['tag_name']

    account = _utils_.httpGetWithCookies('ampm/whoami')

    appPromptOpts = [{
        'type': 'input',
        'name': 'name',
        'message': 'What\'s name?',
        'validate': nameValidate
    }, {
        'type': 'input',
        'name': 'version',
        'default': '1.0.0',
        'message': 'What\'s version?'
    }, {
        'type': 'input',
        'name': 'author',
        'default': account['name'],
        'message': 'What\'s author?'
    }, {
        'type': 'input',
        'name': 'description',
        'message': 'What\'s description?'
    }, {
        'type': 'input',
        'name': 'main',
        'default': 'main.py',
        'message': 'What\'s main?'
    }, {
        'type': 'input',
        'name': 'icon',
        'default': 'icon.png',
        'message': 'What\'s icon?'
    }, {
        'type': 'checkbox',
        'name': 'archicads',
        'message': 'What\'s archicads?',
        'choices': [{
            'name': '22'
        }, {
            'name': '23'
        }],
        'validate': archicadsValidate
    }]

    appPromptRep = PyInquirer.prompt(appPromptOpts)
    appName = appPromptRep['name']
    appRep = _utils_.httpPostWithCookies('amp/init', data={'name': appName})
    appRes = appRep.json()

    # change str to int
    acds = appPromptRep['archicads']
    appPromptRep['archicads'] = []
    for acd in acds:
        appPromptRep['archicads'].append(int(acd))

    appPromptRep['keywords'] = []
    appPromptRep['runtime'] = runtime
    appPromptRep['id'] = appRes['id']
    appPromptRep['sign'] = appRes['sign']

    appDir = path.join(os.getcwd(), appName)
    os.mkdir(appDir)
    mFile = path.join(appDir, 'manifest.json')
    with open(mFile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(appPromptRep, indent=2, ensure_ascii=False))
        f.close()
