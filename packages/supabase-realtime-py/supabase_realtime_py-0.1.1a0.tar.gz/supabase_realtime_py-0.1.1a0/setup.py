#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

history = ""

requirements = ['websockets==8.1']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Supabase",
    author_email='ant@supabase.io',
    python_requires='>=3.5',
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Client for Phoenix Channels",
    download_url="https://github.com/supabase/realtime-py/archive/0.1.1-alpha.tar.gz",
    install_requires=requirements,
    license="MIT license",
    long_description='readme history',
    include_package_data=True,
    keywords='realtime-py',
    name='supabase_realtime_py',
    packages=find_packages(include=['realtime', 'realtime_py.*', 'phoenix channels', 'phoenix', 'channels', 'websockets']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/supabase/realtime-py',
    version='0.1.1-alpha',
    zip_safe=False,
)
