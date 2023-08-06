# tensorflow-modules
tensorflow layers, models

# Requirements
* python >= 3.8.6

# Setup

## create venv

```shell
$ python -m venv $(pwd)
```

## activate venv

```shell
$ source bin/activate
$ pip install -r requirements.txt
```

## deactivate venv

```shell
$ deactivate
```

# test
```shell
$ python -m unittest discover tensorflow_modules
```

# package release

* release

```shell
$ rm -rf tensorflow_modules.egg-info/* dist/*
$ python setup.py sdist bdist_wheel
$ twine upload --repository pypi dist/*
```

* check

```shell
$ open https://pypi.org/project/tensorflow-modules
$ pip --no-cache-dir install --upgrade tensorflow-modules
```
