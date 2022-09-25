import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


setup(
    name="async_pipeline",
    version=read("async_pipeline", "VERSION"),
    description="nothing here",
    url="https://github.com/oSoloTurk/async_pipeline/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="oSoloTurk",
    packages=find_packages(exclude=["tests", ".github"]),
)