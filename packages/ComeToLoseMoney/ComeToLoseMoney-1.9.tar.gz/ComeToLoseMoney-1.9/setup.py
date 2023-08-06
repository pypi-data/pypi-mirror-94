from setuptools import setup

setup(
    name='ComeToLoseMoney',
    version='1.9',
    description='ComeToLoseMoney module',
    author='Arthur',
    author_email='arthur8485@gmail.com',
    packages=['ComeToLoseMoney'],  
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
