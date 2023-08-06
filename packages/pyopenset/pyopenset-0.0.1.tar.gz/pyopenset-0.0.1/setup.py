import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyopenset", # Replace with your own username
    version="0.0.1",
    author="Rafael S. Pereira",
    author_email="r.s.p.models@gmail.com",
    description="Infering novel classes for classification problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/R-S-P-MODELS/pyopenset/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
