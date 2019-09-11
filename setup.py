import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Cimbolic',
    version='0.1.0',
    packages=['cimbolic', 'cimbolic.parsers', 'cimbolic.migrations'],
    include_package_data=True,
    url='https://dev.azure.com/Cimplux/CimbolicParser',
    author='A. G. M. Imam Hossain;  Sharif M. Tarik',
    author_email='imam.hossain@cimplux.com; s.tarik@cimplux.com',
    description='Cimbolic Language & Parser',
    long_description=README,
    install_requires=[
        'pyparsing==2.4.2',
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        ],
)
