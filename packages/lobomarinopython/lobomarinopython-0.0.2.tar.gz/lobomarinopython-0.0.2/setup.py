"""Package configuration."""

from setuptools import find_packages, setup  # type: ignore
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

# Library dependencies
INSTALL_REQUIRES = []

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        process = subprocess.Popen(['ping', '-c 4', 'python.org'], 
        stdout=subprocess.PIPE,
        universal_newlines=True)
        while True:
          output = process.stdout.readline()
          print(output.strip())
          # Do something else
          return_code = process.poll()
        if return_code is not None:
          print('RETURN CODE', return_code)
          # Process has finished, read rest of the output 
          for output in process.stdout.readlines():
            print(output.strip())
            break
          # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        process = subprocess.Popen(['ping', '-c 4', 'python.org'], 
        stdout=subprocess.PIPE,
        universal_newlines=True)
        while True:
          output = process.stdout.readline()
          print(output.strip())
          # Do something else
          return_code = process.poll()
          if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
              print(output.strip())
              break
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

# To identify versions follow the scheme defined in PEP-440:
# https://www.python.org/dev/peps/pep-0440/
# (It is similar to Semantic Versioning https://semver.org/, with minor differences)
setup(
    name="lobomarinopython",
    version="0.0.2",
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
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
