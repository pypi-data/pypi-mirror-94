from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='nse_quadratic_mats',
      version='0.0.2',
      description=('basic routines for treating the NSE with the convection' +
                   ' as a tensor'),
      license="MIT",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Jan Heiland',
      author_email='jnhlnd@gmail.com',
      url="https://gitlab.mpi-magdeburg.mpg.de/heiland/nse-quadratic-mats",
      packages=['nse_quadratic_mats'],  # same as name
      install_requires=['numpy', 'scipy'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          ]
      )
