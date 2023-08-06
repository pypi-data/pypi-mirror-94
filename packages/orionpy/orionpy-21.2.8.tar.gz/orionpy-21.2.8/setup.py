# similarities with requirements.txt
# Gestion de la distribution et de la creation de paquets
from setuptools import setup, find_packages
from os import path

# Gets current path
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

# Gets the version to set from the VERSION file
# Version meets the following : https://www.python.org/dev/peps/pep-0440/#version-scheme
with open(path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name = 'orionpy',  # Required
    version = version,  # content of VERSION file
    description = 'Python API to administrate arcOpole Builder',
    long_description = long_description,  # content of README.md file
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.com/esrifrance-public/orionpy/orionpy',
    author = 'acollange',
    author_email = 'acollange@esrifrance.fr',
    license="Proprietary",
    # Keeps docs and orionpy. Excludes orion[core,gis,csv] to be importable packages
    packages = find_packages(exclude = ['tests', 'test', 'orioncore', 'oriongis', 'orioncsv']),
    install_requires = [
        'requests',
        'urllib3',
    ],
    # Classifiers gives some more information about the project
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'License :: Other/Proprietary License'
    ],
    python_requires='>=3.6',
    # Keywords related to this project
    keywords = 'orionpy orion arcopole builder',
)

