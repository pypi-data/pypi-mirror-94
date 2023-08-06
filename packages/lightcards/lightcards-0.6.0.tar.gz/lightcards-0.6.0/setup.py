from setuptools import setup
from os import path

pwd = path.abspath(path.dirname(__file__))
with open(path.join(pwd, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lightcards",
    version="0.6.0",
    description="Terminal flashcards from Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sr.ht/~armaan/lightcards",
    author="Armaan Bhojwani",
    author_email="me@armaanb.net",
    license="MIT",
    packages=["lightcards"],
    install_requires=["beautifulsoup4", "markdown"],
    data_files=[("man/man1", ["man/lightcards.1"])],
    entry_points={
        "console_scripts": ["lightcards=lightcards:main"],
    },
    classifiers=[
        "Intended Audience :: Education",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
    ],
)
