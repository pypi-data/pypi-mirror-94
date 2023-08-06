from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'READMEFORPYPI.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ComeToLoseMoney',
    version='2.2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='ComeToLoseMoney module',
    author='Arthur',
    author_email='arthur8485@gmail.com',
    packages=find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    python_requires='~=3.3',            
    install_requires=[
        "pendulum>=2.0.5"
        
   ]
)
