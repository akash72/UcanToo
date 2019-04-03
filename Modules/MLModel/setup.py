from setuptools import find_packages
from setuptools import setup

setup(
    name='trainer',
    version='0.7',
    packages=find_packages(),
    install_requires=[
          'keras',
          'tensorflow',
          'h5py'
    ],
    include_package_data=True,
    description='UcanToo trainer package'
    )
