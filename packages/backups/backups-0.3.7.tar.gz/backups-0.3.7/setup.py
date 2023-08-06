from setuptools import setup, find_packages

from backups import version

with open("README.md", "r") as f:
  description = f.read()

setup(
  name="backups",
  version=version.VERSION,
  description="Database backup utility",
  long_description=description,
  long_description_content_type="text/markdown",
  author="ptdorf",
  author_email="ptdorf@gmail.com",
  url="https://github.com/ptdorf/backups",
  download_url="https://github.com/ptdorf/backups/tarball/master",
  keywords="backups backup mysql",
  license="MIT",
  python_requires='>=3',
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
  ],
  packages=find_packages(exclude=["docs", "tests"]),
  install_requires=[
    "docopt",
    "pyyaml>=5.3.1",
    "mysqlclient",
    "requests",
  ],
  entry_points={
    "console_scripts": [
      "backups=backups.cli:main",
    ],
  },
  # scripts=[
  #   "bin/backups-check",
  # ]
)
