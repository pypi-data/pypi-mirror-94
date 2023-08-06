import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="db-edges", # Replace with your own username
    version="0.0.2",
    author="Dan Bean",
    author_email="author@example.com",
    description="A small graph library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeanm/edges",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)