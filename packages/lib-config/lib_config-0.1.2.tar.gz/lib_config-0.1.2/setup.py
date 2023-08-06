from setuptools import setup, find_packages
import sys

setup(
    name='lib_config',
    packages=find_packages(),
    version='0.1.2',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_config.git',
    download_url='https://github.com/jfuruness/lib_config.git',
    keywords=['Furuness', 'Config', 'Wrapper', 'ETL', 'Helper Functions'],
    install_requires=[
        'lib_utils',
        'pytest',
        ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'],
    entry_points={},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
