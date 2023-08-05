import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="karel-for-synthesis",
    version="1.2.0",
    author_email="karel_for_synthesis@kavigupta.org",
    description="Karel Parser and Executor useful for program synthesis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/karel-for-synthesis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["attrs==20.3.0", "numpy", "pylru==1.2.0", "ply==3.11"],
)
