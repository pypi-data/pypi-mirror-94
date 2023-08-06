
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="dataip",
    version="0.0.2",
    description="dataip package is used to gather information based on your IP address",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Aditya Khemka",
    license="MIT",
    keywords=['ip','aditya','khemka','aditya khemka','ipinfo','ip address','python','ipdata','dataip'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dataip"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)