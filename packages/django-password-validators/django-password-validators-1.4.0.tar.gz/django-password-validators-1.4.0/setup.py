import os
from os.path import dirname, realpath
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from django_password_validators import __version__ as VERSION


class Tox(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


__dir__ = realpath(dirname(__file__))

TESTS_REQUIRE = ['tox >= 2.3']

DESCRIPTION = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-password-validators',
    version=VERSION,
    description="Additional libraries for validating passwords in Django.",
    long_description=DESCRIPTION,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Security',
    ],  # strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='django password validator',
    author='Wojciech Banas',
    author_email='fizista@gmail.com',
    url='https://github.com/fizista/django-password-validators',
    license='BSD',
    packages=find_packages(exclude=['tests*', ]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django >= 2.2.8',
    ],
    tests_require=TESTS_REQUIRE,
    extras_require={
        'test': TESTS_REQUIRE,
    },
    cmdclass={'test': Tox},
)
