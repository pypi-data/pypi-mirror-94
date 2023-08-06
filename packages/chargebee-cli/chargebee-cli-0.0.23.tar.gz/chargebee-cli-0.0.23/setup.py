import codecs
import os.path

from setuptools import setup, find_packages

this_file_path = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.23'


def read(*parts):
    return codecs.open(os.path.join(this_file_path, *parts), 'r').read()


install_requires = [
    'click',
    'pyfiglet',
    'colorama',
    'configparser',
    'tqdm',
    'tabulate',
    'requests',
    'pandas',
    'openpyxl',
    "setuptools",
    'wheel'
]

setup_options = dict(
    name='chargebee-cli',
    description='cli for chargebee apis',
    long_description=read('README.rst'),
    author='Nandkishor bhasker',
    author_email='bhasker.nandkishor@gmail.com',
    version=VERSION,
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'cb = chargebeecli.__main__:main'
        ]
    },
    install_requires=install_requires,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['*.yaml', '*.ini', '*.txt']},
)
setup(**setup_options)
