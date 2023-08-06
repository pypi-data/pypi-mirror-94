import os.path
import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setuptools.setup(
    name="podnuit",
    version="1.1",
    author="Olivier Mailhot",
    description="Loup-garou pas de nuit",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gregorpatof/podnuit",
    packages=setuptools.find_packages('.'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)