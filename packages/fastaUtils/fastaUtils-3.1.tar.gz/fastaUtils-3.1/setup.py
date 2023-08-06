from setuptools import setup

setup(name='fastaUtils',
      version='3.1',
      description='fastaUtils',
      url='https://gitlab.com/LBS-EPFL/code/fastautils/-/tree/v3.0',
      author='szamuner',
      author_email='stefano.zamuner@protonmail.com',
      scripts=['bin/fst-awk','bin/fst-download','bin/fst-grep','bin/fst-paste','bin/fst-shuf','bin/fst-cut','bin/fst-encode','bin/fst-logo','bin/fst-profile','bin/fst-sort','bin/fst-distance','bin/fst-fromstockholm','bin/fst-random','bin/fst-split'],
      license='MIT',
      packages=['fastaUtils'],
      zip_safe=False)
