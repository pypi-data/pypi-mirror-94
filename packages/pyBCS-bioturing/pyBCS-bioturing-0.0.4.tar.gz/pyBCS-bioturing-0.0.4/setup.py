import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyBCS-bioturing",
    version="0.0.4",
    author="BioTuring",
    author_email="support@bioturing.com",
    description="Create BioTuring Compressed Study (bcs) file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.bioturing.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
