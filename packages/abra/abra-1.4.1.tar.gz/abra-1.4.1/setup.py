import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abra",
    version="1.4.1",
    # author="",
    author_email="abra.eyetracking@gmail.com",
    description="abra: open-source eye tracking data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abra-eyetracking/abra-eyetracking",
    packages=setuptools.find_packages(),
    install_requires=[
        'abra',
        'numpy',
        'scipy',
        'matplotlib'
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    # python_requires='>=3.6',
)
