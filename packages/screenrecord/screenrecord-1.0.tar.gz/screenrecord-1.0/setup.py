import os
import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="screenrecord",
    version="1.0",
    packages=find_packages(),
    license="Private",
    description="Record screen with python.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="sukhbinder",
    author_email="sukh2010@yahoo.com",
    url = 'https://github.com/sukhbinder/screenrecord',
    keywords = ["screen recording", "windows", "mac", "computer", "python",],
    entry_points={
        'console_scripts': ['record = screenrecord.srecord:main']
    },
	install_requires=["imageio", "imageio-ffmpeg"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
