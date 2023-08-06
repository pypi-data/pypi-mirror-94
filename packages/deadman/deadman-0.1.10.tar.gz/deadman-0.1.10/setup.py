from setuptools import setup, find_packages
from deadman import VERSION

setup(
  name="deadman",
  version=VERSION,
  description="Checks up endpoints and alerts slack",
  long_description="Checks up endpoints and alerts slack when they fail.",
  author="jpedro",
  author_email="ptdorf@gmail.com",
  url="https://github.com/ptdorf/deadman",
  download_url="https://github.com/ptdorf/deadman/tarball/master",
  keywords="monitoring alerts slack http",
  license="MIT",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
  ],
  packages=find_packages(),
  install_requires=[
    "requests",
    "pyyaml",
  ],
  entry_points={
    "console_scripts": [
      "deadman=deadman.cli:main"
    ]
  },
)
