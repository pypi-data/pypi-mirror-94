import setuptools

import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EODHistoricalWrapper",
    packages = ['EODHistoricalWrapper'],
    version="0.0.1c",
    license='MIT',
    author="Chakrit Yau",
    author_email="palmbook@gmail.com",
    description="Wrapper for fetching individual stock information from EODHistorical",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/palmbook/EODHistoricalWrapper",
    download_url = 'https://github.com/palmbook/EODHistoricalWrapper/archive/v0.0.1c.tar.gz',
    keywords = ['EODHistorical', 'Stock', 'Finance'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=install_requires
)