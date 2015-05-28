from setuptools import setup, find_packages

setup(name='exoplanets',
      version='0.0.1',
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


