from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="ProjectWeb",
      version="1.0",
      description="My project gallary",
      packages=find_packages(),
      include_package_data=True, #MANIFEST.in
      install_requires=requirements)