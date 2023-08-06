from setuptools import setup, find_packages

setup(
    name="mamba_toolbox",
    version="1.1.0.11",
    description="Mambalib toolbox",
    install_requires=['click==7.1.2', 'requests==2.25.1'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mamba = mamba.__main__:cli'
        ]
    }
)