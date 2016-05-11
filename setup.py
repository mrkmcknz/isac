from setuptools import setup

setup(
    name="isac",
    version="0.1.0",
    description=("Intent extraction engine."),
    license=("LGPL-3"),
    packages=["isac", "isac.utils"],
    install_requires=[
        "textblob==0.11.1",
        "six==1.10.0"
    ]

)
