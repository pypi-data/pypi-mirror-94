from os import path as os_path
from setuptools import setup, find_packages

this_directory = os_path.abspath( os_path.dirname(__file__) )

# read file contents
def read_file( filename ):
    print( "file name: {}".format( os_path.join( this_directory, filename ) ) )
    with open( os_path.join( this_directory, filename ), encoding='utf-8' ) as f:
        long_description = f.read()
    return long_description

# get the requirements
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='xl_dlframe',  # package name
    python_requires='>=3.4.0',  # python environment
    version='0.0.1',  # package version
    description="Xiuli's deep learning frame.",  # package introduction, shown in the pypi
    long_description = read_file('README.md'),  # read the README.md's contents
    long_description_content_type="text/markdown",  # assign the package text format as markdown
    author="XiuliZhang",  # aothor's information
    author_email='zhangxiuli_nature@126.com',
    url='https://blog.csdn.net/suezhang9?spm=1000.2115.3001.5343',
    # Tell the package information, find_packages() could be ok too
    packages=['xl_dlframe'],
    package_data = {
        'xl_dlframe': ['files.json']
    }, # To read the data file
    install_requires=[
        'numpy',
        'matplotlib',
    ],  # Tells the rellied packages
    include_package_data=True,
    license="MIT",
    keywords=['xl_dlframe'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
    ],
)

