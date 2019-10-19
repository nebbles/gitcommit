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

