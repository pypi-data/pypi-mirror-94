import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="simplecheck",
  version="0.0.4",
  author="Yicas-3111",
  author_email="2556152782@qq.com",
  description="A python program to check all data in a program more easily",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Yicas-3111/Ez_Check",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)