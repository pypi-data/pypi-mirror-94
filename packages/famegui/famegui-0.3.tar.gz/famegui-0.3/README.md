# FAME-GUI

Recommended tools version:
- Python 3.8
- PySide2 for Qt 5.15

```bash
pip3 install -r requirements.txt
```

## Install dev tools on Ubuntu 20.04

```
sudo apt install python3-pyside2.qtwidgets pyqt5-dev-tools qttools5-dev-tools qtcreator
```

## Packaging the app

> Make sure to add in your `~/.pypirc` the credentials required to publish a package on https://pypi.org/project/famegui/

```bash
pip3 install --user -U setuptools twine wheel

# create package (source distribution)
python3 setup.py sdist

# upload to PyPI
twine upload dist/*

# install the published package locally
pip3 install -U famegui
```
