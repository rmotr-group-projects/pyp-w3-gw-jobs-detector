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
    name='rmotr-b8-pyp-g2-jobs-detector',
    version='0.3.1',
    description="rmotr.com Group 2 | Jobs Detector",
    author='Preston R, Sharma N',
    author_email='questions@rmotr.com',
    url = 'https://github.com/prestonr83/pyp-w3-gw-jobs-detector/',
    download_url = 'https://github.com/prestonr83/pyp-w3-gw-jobs-detector/tarball/0.3',
    license='CC BY-SA 4.0 License',
    packages=['jobs_detector'],
    maintainer='rmotr.com',
    tests_require=[
        'pytest==2.9.1'
    ],
    zip_safe=False,
    cmdclass={'test': PyTest},
)
