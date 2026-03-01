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

# Good to know for me : 

# Kode bare minimum (paling dasar) buat ngeresmiin package secara lokal itu cuma segini doang:

# Python
# from setuptools import setup, find_packages

# setup(
#     name="books_recommender",
#     packages=find_packages()
# )

# The reason is Standar Industri (Best Practice) and PEP 8 (Python Enhancement Proposal) menyarankan untuk selalu mengisi metadata yang lengkap pada file setup.py, seperti nama package, versi, penulis, deskripsi, dan lain-lain. 
# Hal ini penting untuk memudahkan pengguna lain dalam memahami apa yang package tersebut lakukan, siapa pembuatnya, dan bagaimana cara menggunakannya. 
# Selain itu, metadata yang lengkap juga membantu dalam proses distribusi dan instalasi package melalui PyPI (Python Package Index) atau platform distribusi lainnya. 

# Jadi, meskipun kode minimal bisa saja bekerja, mengikuti standar industri dan PEP 8 akan membuat package kamu lebih profesional dan mudah digunakan oleh orang lain.