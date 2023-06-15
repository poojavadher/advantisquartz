from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in advantisquartz/__init__.py
from advantisquartz import __version__ as version

setup(
	name="advantisquartz",
	version=version,
	description="Custom App",
	author="pooja@sanskartechnolab.com",
	author_email="pooja@sanskartechnolab.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
