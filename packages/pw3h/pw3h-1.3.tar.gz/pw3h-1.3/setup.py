from distutils.core import setup
import setuptools

setup(name='pw3h',
      version='1.3',
      packages=setuptools.find_packages(),
      data_files=[('', ['ERC20.json', 'UniFactory.json', 'UniPair.json'])]
      )
