import os
from setuptools import setup, find_packages

setup(name='ln2_monitor',
      version='0.3.6',
      description='Plotting data for ln2 masses',
      author='Jordan Wheeler, David Shin',
      author_email='wheeler1711@gmail.com',
      packages=find_packages(),
      url="https://github.com/dav17393/LN2_Monitor",
      #data_files=[(local_samples_dir, sample_data_files),
                  #(local_demos_dir, demo_files)],
      include_package_data=True,
      python_requires='>3.7',
      install_requires=['numpy',
                        'matplotlib>=3.5.2',
                        'pyusb',]
      )
      
      