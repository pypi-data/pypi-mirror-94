from distutils.core import setup

setup(name='pw3h',
      version='1.1',
      py_modules=['pw3h'],
      data_files=[('pw3h', ['pw3h/ERC20.json', 'pw3h/UniFactory.json', 'pw3h/UniPair.json'])]
      )
