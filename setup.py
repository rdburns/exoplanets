from setuptools import setup, find_packages

from exoplanets import __version__

setup(name='exoplanets',
      version=__version__,
      scripts=['exoplanets.py'],

      install_requires=[
          "enum",
          "inflect",
          "colorama",
          "requests"],

      #MetaData:
      description='Commandline viewer for the Open Exoplanet Catalog. http://www.openexoplanetcatalogue.com/',
      url='https://github.com/rdburns/exoplanets',
      author='Ryan Burns',
      author_email='rdburns@gmail.com',
      license='unlicense',
      packages=find_packages(),
      zip_safe=False)


