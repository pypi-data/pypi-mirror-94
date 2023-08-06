import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="24p",
    version="0.0.8",
    author="lingjf",
    author_email="lingjf@gmail.com",
    description="24Point",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lingjf/24p",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            '24p = p24.p24:main',
        ]
    }
)