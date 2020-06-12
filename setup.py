import io
import pathlib
import re

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("githunt/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

# This call to setup() does all the work
setup(
    name="githunt",
    version=version,
    description="Browse most stared Github repositories by date from your command line.",
    long_description=readme,
    python_requires='>3.7',
    long_description_content_type="text/markdown",
    url="https://github.com/SriNandan33/githunt",
    author="Srinivasa Rao",
    author_email="nandusrinivas33.cse@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["githunt"],
    include_package_data=True,
    install_requires=[
        "black==19.10b0",
        "Click==7.0",
        "colorama==0.4.3",
        "pylint==2.4.4",
        "requests==2.22.0",
        "tabulate==0.8.6",
    ],
    entry_points={
        "console_scripts": [
            "githunt=githunt.__main__:search",
        ]
    },
)
