# setup.py for easyserial

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="easyserial",
    version="0.2.0",
    license="MIT",
    author="Matteo Meneghetti",
    author_email="matteo@meneghetti.dev",
    description="Serial protocol to send and receive data effortlessly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/altairLab/elasticteam/forecast/easy-serial",
    packages=setuptools.find_packages(),
    install_requires=["pyserial"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts": [
            "easyserial-logger=easyserial.scripts.logger:main"
        ]
    }
)
