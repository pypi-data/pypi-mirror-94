import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="ratings",
    version="0.0.9",
    description="Basic Elo Rating calculations",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/ratings",
    author="microprediction",
    author_email="pcotton@intechinvestments.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ratings"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["wheel","pathlib","numpy>=1.16.5"],
    entry_points={
        "console_scripts": [
            "ratings=ratings.__main__:main",
        ]
    },
)
