from setuptools import setup

setup(
        packages=['web', 'auth', 'config'],
        entry_points={
            'console_scripts': [ 'main = web:main']
            }
        )
