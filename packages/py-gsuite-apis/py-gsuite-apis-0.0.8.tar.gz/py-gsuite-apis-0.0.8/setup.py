import os
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_requirements():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "requirements.txt")) as f:
        return [l.strip() for l in f]


def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, "version.txt")) as f:
            return f.read().strip()
    except Exception:
        return "0.0.1"


setuptools.setup(
    name="py-gsuite-apis",
    version=get_version(),
    author="Jeff Astor",
    author_email="jeff@astor.io",
    description="Standarize and simplify requests to various GSuite APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jastor11/py-gsuite-apis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    packages=setuptools.find_packages(),
    install_requires=get_requirements(),
    zip_safe=False,
    scripts=[],
    data_files=[],
)
