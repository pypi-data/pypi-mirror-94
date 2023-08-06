from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='bread-tools',
    version='0.0.2',
    description='Basic processing tools in common algorithms.',
    url='https://github.com/Joe-Laue/bread-tools',

    # Author details
    author='Joe',
    author_email='joe.laue@outlook.com',

    # Packages
    packages=['bread.tools.data',
              'bread.tools.file',
              'bread.tools.log',
              'bread.tools.text'],

    # License
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules=["bread-tools"]
)
