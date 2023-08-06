from setuptools import setup, find_packages

setup(
    name='envprotecc',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # TODO add other dependencies here
        'Click',
    ],
    entry_points='''
        [console_scripts]
        protecc=protecc.commands:protecc
    ''',
)
