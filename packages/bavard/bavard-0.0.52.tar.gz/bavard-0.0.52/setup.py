import os
import sys
import setuptools
from setuptools.command.install import install

# The version of this package
VERSION = "0.0.52"


class VerifyVersionCommand(install):
    """
    Custom command to verify that the git tag matches the package version.
    Source: https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
    """

    description = "verify that the git tag matches the package version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = (
                f"Git tag: {tag} does not match the version of this package: {VERSION}"
            )
            sys.exit(info)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bavard",
    version=VERSION,
    author="Bavard AI, Inc.",
    author_email="dev@bavard.ai",
    description="A library and CLI for NLP and chatbot tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bavard-ai/bavard-nlu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["bavard=bavard.__main__:main"],
    },
    install_requires=[
        "transformers==3.4.0",
        "tensorflow==2.2.2",
        "scikit-learn==0.24.1",
        "numpy==1.18.5",
        "tensorflow-probability==0.10.1",
        "uncertainty-metrics==0.0.81",
        "fire==0.4.0",
        "keras-tuner==1.0.2",
        "uvicorn==0.13.3",
        "pydantic==1.7.3",
        "spacy==3.0.1",
        "bavard-ml-common==0.0.14"
    ],
    cmdclass={"verify": VerifyVersionCommand},
)
