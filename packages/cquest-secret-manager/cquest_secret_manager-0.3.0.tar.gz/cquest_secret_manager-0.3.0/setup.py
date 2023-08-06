#!/usr/bin/env python

from setuptools import find_packages, setup


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    line_iterator = (line.strip() for line in open(filename))
    lines = []
    for line in line_iterator:
        if line.startswith("#"):
            continue
        elif line.startswith("git+"):
            repo_name = line.split("/")[-1].split("@")[0]
            lines.append(f"{repo_name} @ {line}")
        else:
            lines.append(line)

    return lines


setup(
    name="cquest_secret_manager",
    version="0.3.0",
    description="python implementation of the functionalities of secret manager",
    author="Ksenija Babarokina",
    author_email="ksenija.b@cquest.ai",
    url="http://gitlab.com/cquest1/cquest_secret_manager",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
    zip_safe=False,
    keywords="cquest_secret_manager",
)
