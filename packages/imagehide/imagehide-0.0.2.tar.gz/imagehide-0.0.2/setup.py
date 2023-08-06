
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="imagehide",
    version="0.0.2",
    description="This was made and developed by techraj (@Teja Swaroop). I've just converted it to a wheel file :)",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Aditya Khemka",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["imagehide"],
    include_package_data=True,
    install_requires=["requests","colorama","commonmark","Pillow","pycryptodome","pyfiglet","Pygments","rich","termcolor","typing-extensions","image","crypto"],
    entry_points={
        "console_scripts": [
            "imagehide=imagehide.__main__:main",
        ]
    },
)