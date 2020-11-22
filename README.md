## Space Station 13 Tools
```
# Note: Install Python 3

# Note: install Poetry for Linux
$: curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Note: install Poetry for Windows
$: (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python

$: python get-poetry.py --uninstall
```

```
$: poetry install  # install all dependencies
```

### dist

```
$: pip install dist/ss13_tools-0.0.1-py3-none.any.whl

$: ss13-tools
```

### docs

```
$: poetry shell
$: cd docs
# Note: review source/conf.py and source/index.rst
$: make html
# Note: see docs in docs/build/apidocs/index.html
```

### ss13_tools

```
$: poetry run python ./ss13_tools/genetic_analyzer.py
$: poetry run python ./ss13_tools/password_analyzer.py ****n o e

$: poetry run python ./ss13_tools/runner.py
```

### tests

```
$: poetry run pytest
```

```
$: poetry run pytest --cov=ss13_tools --cov-report=html tests
#: Note: see coverage report in htmlcov/index.html
```

### poetry.lock

Dependencies, Python version and the virtual environment are managed by `Poetry`.

```
$: poetry search Package-Name
$: poetry add Package-Name[==Package-Version]
```

### pyproject.toml

Define project entry point and metadata.  

### setup.cfg

Configure Python libraries.  

### Linters

```
$: poetry run black .
```

### Publish

```
$: poetry config pypi-token.pypi PyPI-API-Access-Token

$: poetry publish --build
```

```
https://pypi.org/project/ss13-tools/
```
