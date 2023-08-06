try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from textwrap import dedent, fill

def format_desc(desc):
    return fill(dedent(desc), 200)

def format_classifiers(classifiers):
    return dedent(classifiers).strip().split('\n')

def split_keywords(keywords):
    return dedent(keywords).strip().replace('\n', ' ').split(' ')

def file_contents(filename):
    with open(filename) as f:
        return f.read()

setup(
    name = "CloseableQueue-py3",
    version = "0.9.2",
    author = "Ted Tibbetts",
    author_email = "intuited@gmail.com",
    maintainer = "Eric Dramstad",
    maintainer_email = "edrams@gmail.com",
    url = "https://github.com/ejd/CloseableQueue",
    description = format_desc("""
        These classes and functions provide the facility to close a queue
        and to use it as an iterator.
        """),
    long_description = file_contents('README.txt'),
    long_description_content_type = 'text/x-rst',
    classifiers = format_classifiers("""
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: BSD License
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 3
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: Utilities
        """),
    keywords = split_keywords("""
        queue multithreading threading iterator iterable iteration
        """),
    py_modules = ['CloseableQueue'],
    packages = ['CloseableQueue.test'],
    package_dir = {'CloseableQueue': ''},
    test_suite = 'test.make_test_suite',
    )
