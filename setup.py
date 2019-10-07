from os import path
from setuptools import find_packages, setup

# See https://setuptools.readthedocs.io/en/latest/setuptools.html and
# https://github.com/pypa/sampleproject/blob/master/setup.py for details.

root_directory = path.abspath(path.dirname(__file__))
with open(path.join(root_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(root_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()

setup(
    name='Cimbolic',
    version=version,
    description='Cimbolic Language & Parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://dev.azure.com/Cimplux/CimbolicParser',
    author='Cimplux',
    author_email='info@cimplux.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        ],
    packages=find_packages(),
    py_modules=['cimbolic_vars'],
    python_requires='>=3.6',
    install_requires=['pyparsing >=2.4'],
    package_data={'cimbolic': ['management/commands/*']},
    zip_safe=False,
    project_urls={
        'Source': 'https://dev.azure.com/Cimplux/_git/CimbolicParser',
    },
)
