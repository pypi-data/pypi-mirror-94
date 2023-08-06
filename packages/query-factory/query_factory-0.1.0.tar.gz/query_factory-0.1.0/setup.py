import os
from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(HERE, "README.md"), encoding="utf8") as _f:
    readme = _f.read()

with open(os.path.join(HERE, "requirements.txt"), encoding="utf8") as _f:
    reqs = _f.read().split()

setup(
    name="query_factory",
    version="0.1.0",
    packages=find_packages(),
    description="Tool to organize query through factories.",
    long_description=readme,
    include_package_data=True,
    long_description_content_type="text/markdown",
    install_requires=reqs,
    url="https://gitlab.com/dithyrambe/query-factory",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    license="MIT",
)