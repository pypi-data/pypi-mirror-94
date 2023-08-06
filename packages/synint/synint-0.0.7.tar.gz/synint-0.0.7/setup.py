from setuptools import setup

setup(
    name='synint',
    version='0.0.7',
    license='All Rights Reserved.',
    description='synint package',
    py_modules=["synint"],
    install_requires=[
          'numpy',
          'pandas'
      ],
    author = 'Aaron S. Parker',                   # Type in your name
    author_email = 'aparker@hitachisolutions.com',
    package_dir={'':'src'}
)