import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="mt_FileMan",
    version="0.0.2",
    author="mole1000",
    author_email="mole1000@protonmail.com",
    description="A package for custom file managing classes and methods for MaxTrack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='tests',
    extras_require={
        'testing': ['pytest']
    },
)
    
