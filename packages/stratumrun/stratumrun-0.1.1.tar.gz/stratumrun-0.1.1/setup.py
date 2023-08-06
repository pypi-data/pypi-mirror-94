import setuptools

with open("README.md", "r") as handle:
    long_description = handle.read()

setuptools.setup(
    name = "stratumrun",
    version = "0.1.1",
    description = "Stratum Run allows you to run scripts in various languages on the cloud",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author = "Aptus Engineering Inc.",
    author_email = "software@aptusai.com",
    url = "https://bitbucket.org/pinetree-ai/lib-stratum-run-python3",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
    install_requires=[
        'requests',
        'dataclasses',
        'datetime'
    ]
)