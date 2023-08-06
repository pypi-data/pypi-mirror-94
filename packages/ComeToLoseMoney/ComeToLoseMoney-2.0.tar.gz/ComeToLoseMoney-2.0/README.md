# Come To Lose money pip package

## Usage:
```python
pip install ComeToLoseMoney
```
## Documentation
[here](./docs/README.md)

## How to create own package:
Step 1. 
```shell
pip install twine
```
Step 2. 
```shell
python setup.py sdist bdist_wheel
```
Step 3.
```shell
twine check dist/*
```
Step 4. 
```shell
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
Step 5.
```shell
twine upload dist/*
```




