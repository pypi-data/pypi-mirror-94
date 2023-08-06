import pathlib
from setuptools import find_packages, setup
from install_requires import install_requires

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
   name="hopprclient",
   version="0.1.6",
   description="Application to upload datasets to the HOPPR servers",
   author="Jack Cosgrove",
   author_email="jack@hoppr.ai",
   license="MIT",
   url="https://www.hoppr.ai/",
   classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3.6",
   ],
   include_package_data=True,
   install_requires=install_requires,
   packages=find_packages(),
   entry_points={
      "console_scripts": [
         "hopprclient=hopprclient.__main__:main",
      ]
   },
   long_description_content_type="text/markdown",
   long_description=README
)