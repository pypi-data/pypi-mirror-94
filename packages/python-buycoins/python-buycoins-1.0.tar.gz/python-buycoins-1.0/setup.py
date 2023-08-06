import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="python-buycoins",
    version="1.0",
    description="BuyCoins API library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Cimmanuel/python-buycoins",
    author="Immanuel Kolapo",
    author_email="immanuelcaspian@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["requests", "python-decouple"],
)
