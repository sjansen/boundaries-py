# Contributing - boundaries-py

## Development Environment Configuration

```sh
python3 -m venv venv
source venv/bin/activate
python setup.py develop
pip install tox
```

### Using direnv

```sh
direnv allow
```

### Using Multiple Python Versions On macOS

```sh
brew install pyenv
pip install tox-pyenv
cat .python-version | while read VERSION; do
    pyenv install $VERSION
done
```

```sh
# https://github.com/tox-dev/tox/issues/1485
pip install -U virtualenv
virtualenv venv
deactivate
source venv/bin/activate
```
