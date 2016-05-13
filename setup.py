from setuptools import setup, find_packages

setup(
    name="isac",
    version="0.1.0",
    description=("Intent extraction engine."),
    license=("LGPL-3"),
    packages=find_packages(exclude=[]),
    install_requires=[
        "textblob==0.11.1",
        "six==1.10.0"
    ]

)
