from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'testPackage',
    version = '0.1.2',
    keywords = ('seismic', 'signal'),
    description = 'seismic wave analysis',
    license = 'MIT License',

    author = 'Junjun Guo',
    author_email = 'guojj_ce@163.com',
	url='https://github.com/Junjun1guo/seismicWaveAnalysis',
    packages = find_packages(),
	install_requires=['wxPython','numpy'],
    platforms = 'any',
)