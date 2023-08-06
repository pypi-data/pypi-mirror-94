from genericpath import exists
import re
from setuptools import setup, find_packages

mainfile = open('mamba/__init__.py', 'r', encoding='utf-8').read()
appversion = re.findall(r'__version__\s?=\s?\((\d+,\d+,?\d*,?\d*)\)\s?', mainfile)[0].split(',')

setup(
    name="mamba_toolbox",
    version=".".join(appversion),
    description="Mambalib toolbox",
    install_requires=['click==7.1.2', 'requests==2.25.1', 'virtualenv==20.2.2'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mamba = mamba.__main__:cli'
        ]
    }
)