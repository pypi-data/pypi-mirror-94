from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
  readme = readme_file.read()

requirements = ['Pillow']

setup(
  name="pymlutils",
  version="1.1.4",
  author="Grant Backes",
  author_email="gsbackes@gmail.com",
  description="Various functions useful for python and machine learning. Keep your code clean.",
  long_description=readme,
  long_description_content_type="text/markdown",
  url="https://gitlab.com/baka-san/pymlutils",
  packages=find_packages(),
  install_requires=requirements,
  classifiers=[
      "Programming Language :: Python :: 3.6"
  ],
)