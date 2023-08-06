from setuptools import setup, find_packages
from os import path

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

VERSION = '0.0.3'
DESCRIPTION = 'HighDim is a numerical package for computing the marginal density distribution.'


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()




# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="HighDim",
    version=VERSION,
    author="Lily Young",
    author_email="lilyyoung1122@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    url='https://github.com/liyo6397/high_dimensional_density',

    keywords=['python', 'high dimensional data'],
    classifiers=[
    'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)