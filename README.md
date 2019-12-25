<p  align="center">
  <strong>gitcommit</strong>
  <br>
  <code>a tool for writing conventional commits, conveniently</code>
  <br><br>
  <a href="https://badge.fury.io/py/conventional-commit"><img src="https://badge.fury.io/py/conventional-commit.svg" alt="PyPI version" height="18"></a>
  <a href="https://travis-ci.org/nebbles/gitcommit/branches"><img src="https://travis-ci.org/nebbles/gitcommit.svg?branch=master" alt="Travis CI build" height="18"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" height="18"></a>
</p>


# Install

To install

```
pip install conventional-commit
```

To use, run the following command from within a git repository

```
gitcommit
```

# Overview

The purpose of this utility is to expedite the process of committing with a conventional message format in a user friendly way. This tool is not templated, because it sticks rigidly to the [Conventional Commit standard](https://www.conventionalcommits.org), and thus not designed to be 'altered' on a case by case basis.

Commit messages produced follow the general template:
```
<type>[(optional scope)]: <description>

[BREAKING CHANGE: ][optional body / required if breaking change]

[optional footer]
```

Additional rules implemeted:

1. Subject line (i.e. top) should be no more than 50 characters.
2. Every other line should be no more than 72 characters.
3. Wrapping is allowed in the body and footer, NOT in the subject.

# Development

The old distribution method is documented in
[docs/dev_distibution_legacy.md](docs/dev_distribution_legacy.md)

*Note: if modifying `.travis.yml` you should verify it by running `travis lint .travis.yml`*

## Getting started

1. Make sure you have [pre-commit](https://pre-commit.com/#install) installed.

1. Make sure you have [pyenv](https://github.com/pyenv/pyenv) installed.

1. Make sure you have [Poetry](https://github.com/sdispater/poetry) installed.

1. `git clone`

1. `pre-commit install`

1. It is highly recommend you enable setting for storing the venvs within your projects.
    ```
    poetry config settings.virtualenvs.in-project true
    ```

1. Install project dependencies.
    ```
    poetry install
    ```

## Running the package locally

1. Activate the virtual environment.
    ```
    source .venv/bin/activate
    ```

1. Run the package as a module.
    ```
    python -m gitcommit
    ```

Alternatively,

1. Run the package using Poetry's venv as context
    ```
    poetry run python -m gitcommit
    ```

Or, if in another directory,

1.  ```
    ~/GitHub/gitcommit/.venv/bin/python -m gitcommit
    ```

## Deploy

Deployment is handled automatically by Travis CI. It has been linked to the
repository and is automatically watching for pushes to master. It will build and
test every commit to master. It will also build every tagged commit as if it was
a branch, and since its a tagged commit, will attempt to publish it to PyPI.

1. Don't forget to increment version number set in `pyproject.toml`. This can be
   done with poetry.
   ```
   poetry version [patch|minor|major]
   ```

1. Tag the commit (by default applies to HEAD commit - make sure you are on the latest `develop` commit).
   ```
   git tag v#.#.#
   ```

1. When pushing commits to remote, you must explicitly push tags too.
   ```
   git push origin --tags
   ```

## Acknowledgements

This work takes inspiration from [another repository porting Commitizen to Python](https://github.com/Woile/commitizen). This repository however uses none of the same source code and is focusing on a different approach.

## License

This work is published under [GNU GPLv3](./LICENSE).
