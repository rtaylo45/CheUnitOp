from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

setup(
    name='CheUnitOp',
    version='0.0.1',
    packages=find_packages(),
    description='Python library for simulating chemical engineering unit operations',
    author='Zack Taylor',
    platforms=["Linux", "Mac OS-X"],
    #build_requires=['numpy>=1.8.0', 'setuptools'],
    install_requires=['numpy', 'scipy', 'matplotlib'],
    package_data={'': ['*.txt']},
    license='Apache License, version 2.0',
    author_email='rztaylor5@gmail.com'
)

