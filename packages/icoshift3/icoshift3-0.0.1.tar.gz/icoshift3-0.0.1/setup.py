#!/usr/bin/env python
# coding=utf-8

import setuptools

setuptools.setup(
    name="icoshift3", # Replace with your own username
    version="0.0.1",
    author="Charley Western",
    author_email="westernj@lafayette.edu",
    description="Spectral Icoshift updated for python v.3",
    url="https://github.com/JonWestern/icoshift3.git",
   
    python_requires='>=3.0',


    packages=['icoshift3'],
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
    exclude_package_data={'': ['README.txt']},

    install_requires=[
            'numpy>=1.7.1',
            'scipy>=0.12.0',
            ],

    keywords='bioinformatics metabolomics research analysis science',
    license='GPL',
    classifiers=['Development Status :: 4 - Beta',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 2',
               'License :: OSI Approved :: BSD License',
               'Topic :: Scientific/Engineering :: Bio-Informatics',
               'Intended Audience :: Science/Research',
               'Intended Audience :: Education',
              ],

    )
