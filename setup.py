import os
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["tests/"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import sys, pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='rmotr-b9-c1-g5-jobs-detector',
    version='0.0.1',
    description="rmotr.com Group Project | Jobs Detector",
    author='Delio Castillo',
    author_email='jangeador@gmail.com',
    license='CC BY-SA 4.0 License',
    packages=['jobs_detector'],
    maintainer='rmotr.com',
    install_requires=[
        'bs4>=0.0.1',
        'click>=6.6',
        'requests_cache>=0.4.12'
    ],
    tests_require=[
        'pytest==2.9.1'
    ],
    zip_safe=False,
    cmdclass={'test': PyTest},
)
