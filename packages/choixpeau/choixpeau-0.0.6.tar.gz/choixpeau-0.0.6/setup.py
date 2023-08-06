import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def dependencies():
    import os
    """
    Obtain the dependencies from requirements.txt.
    """
    with open('requirements.txt') as reqs:
        return reqs.read().splitlines()

setuptools.setup(
    name="choixpeau",
    version="0.0.6",
    author="Keurcien Luu",
    author_email="keurcien@appchoose.io",
    description="Efficiently assign users to buckets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "redis"
    ]
)