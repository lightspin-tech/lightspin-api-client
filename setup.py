from __future__ import absolute_import
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lightspin_api_client",
    version="0.0.7",
    author="lightspin",
    author_email="support@lightspin.io",
    description="Lightspin API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lightspin-tech/lightspin-api-client",
    install_requires=[
        "datetime",
        "retry",
        "requests",
        "datadog_api_client",
        "elasticsearch",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
