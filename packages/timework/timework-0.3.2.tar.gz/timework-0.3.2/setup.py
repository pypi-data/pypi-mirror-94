import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timework",
    version="0.3.2",
    author="bugstop",
    author_email="pypi@isaacx.com",
    description="measure / limit the function execution time, cross-platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bugstop/python-timework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
