import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymobility", # Replace with your own username
    version="0.0.5.1",
    author="Suraj Regmi",
    author_email="regmi125@gmail.com",
    description="Python mobility library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datapartnership/covid19-migration-south-asia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)