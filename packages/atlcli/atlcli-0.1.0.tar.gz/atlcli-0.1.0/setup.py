import re
import os
from setuptools import setup, find_packages

deps = [
    'click',
    'atlassian-python-api',
    'pyyaml',
    'prettytable',
    'semantic-version',
    'pprint36',
    'requests'
]

version = ""
github_ref = os.getenv('GITHUB_REF')
if github_ref is not None:
    m = re.search(
        "(([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?)", github_ref)
    if m:
        version = m.group(1)
else:
    version = "dev"

setup(
    name='atlcli',
    version=version,
    packages=find_packages(),
    py_modules=['cli', "commands"],
    include_package_data=True,
    install_requires=deps,
    entry_points='''
        [console_scripts]
        atlcli=cli.app:cli
    ''',
)
