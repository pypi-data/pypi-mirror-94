
from setuptools import setup

with open("./README.md", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "litron",
    version = "0.0.0",
    description = "nlp tool",
    author = "team_LITRON",
    author_email = "dummy@dummy.com",
    url = "https://github.co.jp/",
    packages = ["litron"],
    install_requires = [],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "CC0 v1.0",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    ],
    # entry_points = ""
)
