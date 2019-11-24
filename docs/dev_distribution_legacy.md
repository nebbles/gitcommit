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

### setup.py

The setup.py file was configured as follows. This has now changed in favour of
the Poetry build system.

```python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conventional-commit",
    version="0.0.1",
    author="nebbles",
    description="a tool for writing conventional commits, conveniently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nebbles/gitcommit",
    classifiers=[  # https://pypi.org/classifiers/
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ['gitcommit = gitcommit.gitcommit:main']
    },
)
```
