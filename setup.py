from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## Edit variable di bawah ini sesuai dengan project kamu
REPO_NAME = "End-to-End-Book-Recommendation-System"
AUTHOR_USER_NAME = "Zendin110206"
SRC_REPO = "books_recommender"
LIST_OF_REQUIREMENTS = []

setup(
    name=SRC_REPO,
    version="0.0.1",
    author="Muhammad Zaenal Abidin Abdurrahman",
    description="A small local package for ML based books recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="zaenal.abidin110206@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.9",
    install_requires=LIST_OF_REQUIREMENTS
)