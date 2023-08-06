from setuptools import setup

setup(
    name='koyias',
    version='0.1.1',
    py_modules=['koyias'],
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        koyias=koyias:koyias
    ''',
)
