from setuptools import setup

setup(
    name='koyias',
    version='0.1.0',
    py_modules=['koyias'],
    install_requires=[
        'koyiasdep',
    ],
    entry_points='''
        [console_scripts]
        koyias=koyias:koyias
    ''',
)
