"""Package configuration."""

from setuptools import find_packages, setup  # type: ignore
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess


class PreDevelopCommand(develop):
    """Pre-installation for development mode."""
    def run(self):
        subprocess.call(["ECHO", "BBBBBBBBBBB"], shell=True)
        develop.run(self)
        subprocess.call(["ECHO", "AAAAAAAAA"], shell=True)

class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        subprocess.call(["ECHO", "AAAAAAAAA"], shell=True)
        install.run(self)
        subprocess.call(["ECHO", "AAAAAAAAA"], shell=True)


# Library dependencies
INSTALL_REQUIRES = []

# To identify versions follow the scheme defined in PEP-440:
# https://www.python.org/dev/peps/pep-0440/
# (It is similar to Semantic Versioning https://semver.org/, with minor differences)
setup(
    name="lobomarinopython",
    version="0.0.3",
    description="Lobillo",
    author="guillermo castanon",
    author_email="guillermo.h.castanon18@gmail.com",
    url="https://github.com/sahil-rajput/excel2jsonapi",
    packages=find_packages(),
    python_requires=">=3.6",
    setup_requires=["wheel"],
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
    ],
  cmdclass={
        'develop': PreDevelopCommand,
        'install': PreInstallCommand,
    },
)
