from distutils.core import setup
from setuptools import find_packages

setup(
    name='CheUnitOp',
    version='0.0.1',
    description='Python library for simulating chemical engineering unit operations',
    author='Zack Taylor',
    platforms=["Linux", "Mac OS-X"],
    install_requires=['numpy', 'scipy', 'matplotlib'],
    #package_dir={'': 'CheUnitOp'},
    packages=find_packages(),
    include_package_data=True,
    license='Apache License, version 2.0',
    author_email='rztaylor5@gmail.com'
)

