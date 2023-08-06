from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name="cleaninsights",
    version="0.0",
    packages=find_packages(exclude=['docs']),
    install_requires=install_requires,
    author="Iain Learmonth / Guardian Project",
    author_email="iain@learmonth.me",
    description=("CleanInsights gives developers a safe, sustainable, and "
                 "secure way to gather insights about their users using "
                 "cutting edge techniques like differential privacy, onion "
                 "routing, certificate pinning and more."),
    long_description=long_description,
    keywords="privacy metrics analytics",
    url="https://gitlab.com/cleaninsights/clean-insights-python-sdk/",
    project_urls={
        "Bug Tracker":
        "https://gitlab.com/keanuapp/clean-insights-python-sdk/-/issues",
        "Source Code": "https://gitlab.com/keanuapp/clean-insights-python-sdk",
    },
    classifiers=["License :: OSI Approved :: BSD License"],
    test_suite='nose.collector',
)
