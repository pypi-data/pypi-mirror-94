from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cygnsslib',
    version='1.1.6',
    author='Amer Melebari and James D. Campbell',
    author_email='amelebar@usc.edu',
    description='Toolset for working with CYGNSS data and downloading CYGNSS data from PODAC',
    long_description=long_description,
    # install_requires=['geographiclib', 'lxml', 'matplotlib', 'netcdf4', 'numpy', 'pandas', 'pbkdf2', 'pycrypto', 'tqdm', 'xlrd', 'xlwt'],
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/usc_mixil/cygnsslib',
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", exclude='cygnsslib.data_downloader'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
