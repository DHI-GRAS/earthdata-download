from setuptools import setup, find_packages

setup(
    name='earthdata_download',
    version='0.8',
    description='NASA EarthData download interface',
    author='Jonas Solvsteen',
    author_email='josl@dhigroup.com',
    url='https://www.dhi-gras.com',
    packages=find_packages(),
    install_requires=open('requirements_full.txt').read().splitlines())
