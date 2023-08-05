# !/usr/bin/env python
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements-dev.txt') as f:
    test_requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as buf:
    version = buf.read()

setuptools.setup(
    name="cyjax-vectra-integration",
    version=version,
    license="MIT",
    description="cyjax-vectra-integration provides an integration to send indicators to Vectra Brain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cyjax Ltd.",
    author_email="github@cyjax.com",
    url="https://www.cyjax.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities"
    ],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    extras_require={
        'test': test_requirements
    },
    scripts=[
        'bin/cyjax-vectra-integration',
    ]
)
