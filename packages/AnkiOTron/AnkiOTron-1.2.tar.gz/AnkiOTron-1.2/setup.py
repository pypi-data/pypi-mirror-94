import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AnkiOTron",
    version="1.2",
    author="Daniel de Mattos Passy",
    author_email="daniel.passy@gmail.com",
    description="Wrapper around genaki to automate Anki deck creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielpassy/Anki-CardOTron",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)