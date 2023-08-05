import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="serverhttp", 
    version="1.6",
    author="Allen",
    author_email="allen.haha@hotmail.com",
    description="A simple HTTP server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["asyncio"],
    python_requires='>=3.3',
)
