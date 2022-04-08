from setuptools import setup, find_packages


setup(
    name='sfsd',
    version='1.0',
    license='MIT',
    author="Ouassim Hamdani",
    author_email='o_hamdani@estin.dz',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Ouassim-Hamdani/SFSD',
    keywords='SFSD,file structure, ouassim, hamdani, python file,file handle',
    install_requires=[
          'texttable',
      ],

)
