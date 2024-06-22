from pathlib import Path
from setuptools import setup, find_packages
import json


install_requires = [
    "python-dotenv"
]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Games/Entertainment",
    "Topic :: Games/Entertainment :: Board Games"
]


def get_version():
    with open("config/version.json", "r") as f:
        version = json.load(f)
        return f"{version['major']}.{version['minor']}.{version['patch']}"


setup(
    name="pkrhistoryparser",
    version=get_version(),
    author="Alexandre MANGWA",
    author_email="alex.mangwa@gmail.com",
    description="A poker package to parse Hand histories into json objects",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/manggy94/PokerHistoryParser",
    project_urls={
        "Bug Tracker": "https://github.com/manggy94/PokerHistoryParser/issues",
        "Documentation": "https://pkrhistoryparser.readthedocs.io/en/latest/parser/"
    },
    classifiers=classifiers,
    packages=find_packages(exclude=["tests", ".venv", "venv", "venv.*"], include=["pkrhistoryparser"]),
    python_requires=">=3.9",
    install_requires=install_requires,
    license="MIT",
)
