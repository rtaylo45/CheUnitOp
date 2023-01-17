from distutils.core import setup

setup(
    name='CheUnitOp',
    version='0.0.1',
    description='Python library for simulating chemical engineering unit operations',
    author='Zack Taylor',
    platforms=["Linux", "Mac OS-X"],
    install_requires=['numpy', 'scipy', 'matplotlib'],
    packages=['CheUnitOp'],
    license='Apache License, version 2.0',
    author_email='rztaylor5@gmail.com'
)

