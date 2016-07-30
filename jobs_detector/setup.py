from setuptools import setup

setup(
    name='jobs_detector',
    version='0.1',
    py_modules=['jobs_detector'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        jobs_detector=main:cli
    ''',
)