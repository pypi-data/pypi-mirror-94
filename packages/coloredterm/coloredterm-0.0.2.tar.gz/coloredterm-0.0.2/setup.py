import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coloredterm",
    version="0.0.2",
    author="Hostedposted",
    author_email="hostedpostedsite@gmail.com",
    description="Color the text in your terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hostedposted/coloredterm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["Pillow==8.1.0"],
    python_requires='>=3.7',
)