from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='fastaUtils',
      version='1.0.0',
      description='A set of scripts to ease the process of manipulating fasta files',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitlab.com/LBS-EPFL/code/fastautils/-/tree/v3.0',
      author='szamuner',
      author_email='stefano.zamuner@protonmail.com',
      scripts=['bin/fst-awk','bin/fst-download','bin/fst-grep','bin/fst-paste','bin/fst-shuf','bin/fst-cut','bin/fst-encode','bin/fst-logo','bin/fst-profile','bin/fst-sort','bin/fst-distance','bin/fst-fromstockholm','bin/fst-random','bin/fst-split'],
      license='MIT',
      packages=['fastaUtils'],
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
      ],
      python_requires='>=3.6',
    )
