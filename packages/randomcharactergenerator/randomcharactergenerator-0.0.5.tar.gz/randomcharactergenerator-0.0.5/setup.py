import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randomcharactergenerator",
    version="0.0.5",
    author="HighlyIntelligentBeing",
    author_email="highlyintelligentbeing1707@gmail.com",
    description="A library which generates random character codes using the random module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SupremeCoder1707/randomcharactergenerator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
