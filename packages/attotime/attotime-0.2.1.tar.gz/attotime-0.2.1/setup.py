import sys

from os import path
from setuptools import setup, find_packages

TESTS_REQUIRE = []

#Mock is only required for Python 2
PY2 = sys.version_info[0] == 2

if PY2:
    TESTS_REQUIRE.append('mock>=2.0.0')

with open(path.join('attotime', 'version.py')) as f:
    exec(f.read())

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.rst')) as f:
    README_TEXT = f.read()

setup(
    name='attotime',
    version=__version__,
    description='Arbitrary precision datetime library.',
    long_description=README_TEXT,
    long_description_content_type='text/x-rst',
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/attotime',
    packages=find_packages(),
    test_suite='attotime',
    tests_require=TESTS_REQUIRE,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='datetime decimal',
    project_urls={
        'Documentation': 'https://attotime.readthedocs.io',
        'Source': 'https://bitbucket.org/nielsenb/attotime',
        'Tracker': 'https://bitbucket.org/nielsenb/attotime/issues'
    }
)
