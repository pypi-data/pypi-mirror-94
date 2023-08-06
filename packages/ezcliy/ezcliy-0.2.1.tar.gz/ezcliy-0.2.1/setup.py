from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    install_requires=[
        "colorama>=0.4.0", "pyyaml>=5.0.0"
    ],
    name="ezcliy",
    version="0.2.1",
    packages=["ezcliy"],
    project_urls={
        "Repository": "https://github.com/kpostekk/ezcliy/",
        "Docs": "https://ezcliy.readthedocs.io/en/latest/",
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
    python_requires=">=3.9",
)
