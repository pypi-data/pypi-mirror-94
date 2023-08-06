#!/usr/bin/env python

from distutils.core import setup

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

with open("README.md") as f:
    LONG_DESCRIPTION, LONG_DESC_TYPE = f.read(), "text/markdown"


setup(name='DAC43608',
      version='0.2',
      description='A python wrapper for interacting with the DAC43608',
      author='Cam Davidson-Pilon',
      author_email='cam@pioreactor.com',
      url='https://github.com/Pioreactor/DAC43608',
      packages=['DAC43608'],
      license="MIT",
      python_requires=">=3.6",
      install_requires=REQUIREMENTS,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
     )