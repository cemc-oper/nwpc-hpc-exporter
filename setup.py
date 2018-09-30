from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nwpc-hpc-exporter',

    version='0.2.0',

    description='An HPC exporter for NWPC',
    long_description=long_description,

    url='https://github.com/perillaroc/nwpc-hpc-exporter',

    author='perillaroc',
    author_email='perillaroc@gmail.com',

    license='GPL-3.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Systems Administration'
    ],

    keywords='nwpc hpc exporter',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    include_package_data=True,

    install_requires=[
        'click',
        'paramiko',
        'pyyaml',
        'prometheus-client'
    ],

    extras_require={
        'test': ['pytest'],
    },

    entry_points={
        'console_scripts': [
            'disk_space_exporter=nwpc_hpc_exporter.disk_space.exporter:main',
            'disk_usage_exporter=nwpc_hpc_exporter.disk_usage.exporter:main',
            'workload_exporter=nwpc_hpc_exporter.workload.exporter:main',
        ]
    }
)
