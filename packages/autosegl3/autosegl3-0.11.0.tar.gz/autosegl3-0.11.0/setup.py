#!/usr/bin/env python

import os

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['barbell2', 'nibabel', 'tensorflow', 'numpy', 'h5py', 'pydicom']

setup_requirements = []

test_requirements = []

setup(
    author="Ralph Brecheisen",
    author_email='ralph.brecheisen@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="""Tool for automatically segmenting muscle and fat tissue in CT images acquired at the 
    3rd vertebral level""",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='autosegl3',
    name='autosegl3',
    packages=find_packages(include=['autosegl3', 'autosegl3.*']),
    entry_points={
        'console_scripts': [
            'autosegl3=autosegl3.autosegl3:main',
        ],
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbrecheisen/autosegl3',
    version=os.environ['VERSION'],
    zip_safe=False,
)
