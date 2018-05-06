from setuptools import setup

setup(
    name='nagbot',
    packages=['nagbot'],
    include_package_data=True,
    install_requires=[
        'flask',
        'slackclient'
    ],
)