import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mur",
    version="0.0.1",
    author="Oleksandr Litus",
    author_email="oleks.litus@gmail.com",
    description="Opinionated Python manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olitus/mur",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
