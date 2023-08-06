import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unreadable",
    version="0.0.1",
    author="greatusername",
    author_email="alexander.destefano@gmail.com",
    description="An encoder and decoder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathstar13/unreadable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.1',
)