import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torgrims",
    version="0.0.1",
    author="Tomas Torgrimsby",
    author_email="torgrimsatpypi@gmail.com",
    packages=["torgrims_pkg"],
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nrk.no",
    license="OSI Approved (new BSD)",
    python_requires=">=3.6",
    install_requires=[
        "Django>=2.0",
        "pandas",
        "numpy",
    ]
)
