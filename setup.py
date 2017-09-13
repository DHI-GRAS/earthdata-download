from setuptools import setup, find_packages

setup(
    name='earthdata_download',
    version='0.7',
    description='NASA EarthData download interface',
    author='Jonas Solvsteen',
    author_email='josl@dhi-gras.com',
    url='https://www.dhi-gras.com',
    packages=find_packages(),
    install_requires=['requests', 'tqdm'])
