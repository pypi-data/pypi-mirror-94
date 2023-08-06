from setuptools import setup, find_packages

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
VERSION = '0.0.1'
DESCRIPTION = 'HighDim is a numerical package for computing the marginal density distribution.'
LONG_DESCRIPTION = 'HighDim is a numerical package for computing the marginal density distribution.'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()



# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="HighDim",
    version=VERSION,
    author="Lily Young",
    author_email="<lilyyoung1122@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],

    keywords=['python', 'high dimensional data'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)