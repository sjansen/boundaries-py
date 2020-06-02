"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='boundaries',

    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',

    description='Check and enforce code organization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sjansen/boundaries-py',
    author='Stuart Jansen',
    author_email='sjansen@buscaluz.org',

    # https://pypi.org/classifiers/
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='import policy project layout',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['parso'],
    entry_points={
        'console_scripts': [
            'py.boundaries=boundaries:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/sjansen/boundaries-py/issues',
        'Source': 'https://github.com/sjansen/boundaries-py/',
    },
)
