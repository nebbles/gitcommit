<p  align="center">
  <strong>gitcommit</strong>
  <br>
  <code>a tool for writing conventional commits, conveniently</code>
  <br><br>
  <a href="https://badge.fury.io/py/conventional-commit"><img src="https://badge.fury.io/py/conventional-commit.svg" alt="PyPI version" height="18"></a>
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

For development, see the developer readme file: [README.dev.md](./README.dev.md)
