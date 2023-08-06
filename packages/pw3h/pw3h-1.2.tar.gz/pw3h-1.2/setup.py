from distutils.core import setup
import setuptools

setup(name='pw3h',
      version='1.2',
      packages=setuptools.find_packages(),
      data_files=[('pw3h', ['pw3h/ERC20.json', 'pw3h/UniFactory.json', 'pw3h/UniPair.json'])]
      )
