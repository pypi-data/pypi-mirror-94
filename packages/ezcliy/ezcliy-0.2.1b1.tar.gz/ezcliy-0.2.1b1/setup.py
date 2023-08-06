from setuptools import setup
from ezcliy import __version__


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    install_requires=["colorama==0.4.4", "pyyaml==5.4.1"],
    name="ezcliy",
    version=__version__,
    packages=["ezcliy"],
    project_urls={
        'Repository': 'https://github.com/kpostekk/ezcliy/',
        'Docs': 'https://ezcliy.readthedocs.io/en/latest/'
    },
    url="https://github.com/kpostekk/ezcliy",
    license="Apache",
    author="Krystian Postek",
    author_email="krystian@postek.eu",
    description="Framework for creating CLI tools",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9"
)
