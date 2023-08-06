catbhkrcfxksxnek
================
This is a bogus package used to test vulnerabilities in dependency resolution.

_Never use this package for anything!_


```bash
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```