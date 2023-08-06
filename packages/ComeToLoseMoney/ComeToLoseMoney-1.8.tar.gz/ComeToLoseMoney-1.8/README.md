# Come To Lose money pip package

## Usage:
```python
pip install ComeToLoseMoney
```

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

## Documents:
`ComeToLoseMoney.utils`
```python
Date.range(start_date, end_date, format, units)
```




