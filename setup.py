import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="battle-simulator",
    version="0.0.1",
    author="Richard Stoeffel",
    author_email='richard@fake.com',
    description="My short description",
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "pytest-clarity",
            'mock;python_version<"3.3"']
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["PyYAML", "other_packages"],
    url="https://github.com/gene1wood/projectname",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)