# Deployment

The following instructions explain how this command-line application is
distributed. We deploy our builds to the Python Package Index for distribution.
This allows users to install the application with a simple 
`pip install conventional-commit`.

First ensure necessary packages are installed
```
pip install setuptools wheel twine
```

## Testing Distribution

Build the distribution files
```
python setup.py sdist bdist_wheel
```

Upload to the Test Package Index (you will need your unique and seperate
credentials set up for that site)
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --skip-existing
```

If you haven't already, create a virtual env in the `env/` directory
```
python -m venv env
```

Activate the virtual environment
```
source env/bin/activate
```

Install/upgrade the test package that exists on the Test Package Index
```
pip install --upgrade --index-url https://test.pypi.org/simple/ conventional-commit
```

## Official Distribution

Build the distribution files
```
python setup.py sdist bdist_wheel
```

Upload to the Python Package Index
```
twine upload dist/* --skip-existing
```

Install/upgrade the package locally
```
pip install --upgrade conventional-commit
```
