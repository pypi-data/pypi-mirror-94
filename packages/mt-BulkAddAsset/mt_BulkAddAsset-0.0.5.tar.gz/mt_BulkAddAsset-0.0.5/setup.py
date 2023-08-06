import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="mt_BulkAddAsset",
    version="0.0.5",
    author="mole1000",
    author_email="mole1000@protonmail.com",
    description="A package for adding assets to Met/Track",
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
    install_requires='PyQt5>=5',
    include_package_data=True,
    test_suite='tests',
    extras_require={
        'testing': ['pytest']
    },
)
