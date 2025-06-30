#!/usr/bin/env python3
"""
Setup script for Nash Equilibrium Finder
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nash-equilibrium-finder",
    version="1.0.0",
    author="Tomas Ortega and Pablo Mueller",
    author_email="contact@nashequilibrium.dev",
    description="A Python library for analyzing 2-player normal form games and finding Nash equilibria",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/NashEquilibriumFinder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "mypy>=0.900",
        ],
        "web": [
            "flask>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nash-file=nash_file:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yml", "*.yaml", "*.md"],
    },
)
