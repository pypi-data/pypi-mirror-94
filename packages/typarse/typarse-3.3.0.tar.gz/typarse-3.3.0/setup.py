from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='typarse',
    version='3.3.0',
    packages=find_packages(),
    url='https://github.com/redtachyon/typarse',
    license='GNU GPLv3',
    author='RedTachyon',
    author_email='ariel.j.kwiatkowski@gmail.com',
    description='A simple type-hint-based argument parsing library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
      "Programming Language :: Python :: 3.8",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: OS Independent"
    ],
    extras_require={
        "tests": [
            "pytest",
        ]
    }
)
