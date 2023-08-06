from distutils.core import setup
from setuptools import setup
import os

def _load_famegui_version():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    init_filepath = os.path.join(this_dir, "famegui", "__init__.py")

    with open(init_filepath) as f:
        for line in f.readlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string in {}".format(init_filepath))

VERSION = _load_famegui_version()

setup(
    name='famegui',
    packages=['famegui', 'famegui.models'],
    version=VERSION,
    license='Apache',
    description='Graphical user interface to the FAME modelling framework',
    author='Aurélien Regat-Barrel',
    author_email='pypi@cyberkarma.net',
    url='https://gitlab.com/fame2/FAME-Gui',
    download_url='https://gitlab.com/fame2/FAME-Gui/-/archive/v{}/FAME-Gui-v{}.tar.gz'.format(VERSION, VERSION),
    install_requires=[
        'coloredlogs',
        'python-igraph',
        'pyyaml',
        'PySide2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'famegui=famegui.app:run',
        ],
    },
    package_data={
        'famegui': ['data/*'],
    },
)
