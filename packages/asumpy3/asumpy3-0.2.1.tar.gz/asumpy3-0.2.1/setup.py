from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="asumpy3", # Replace with your own username
    version="0.2.1",
    author="Pyxis(Anvay Arora)",
    author_email="artificial.remote.consciousness@gmail.com",
    description="A Mathematical Tool to calculate angle sum property",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)