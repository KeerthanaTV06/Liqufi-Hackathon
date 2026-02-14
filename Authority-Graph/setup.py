"""
Setup configuration for PointZero Member C Authority Graph Builder
"""

from setuptools import setup, find_packages # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pointzero-member-c-authority-graph",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Member C: Pure transformation layer for PointZero irreversibility analysis pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeerthanaTV06/Liqufi-Hackathon",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="blockchain authority graph transformation deterministic ethereum approval security",
    project_urls={
        "Bug Reports": "https://github.com/KeerthanaTV06/Liqufi-Hackathon",
        "Source": "https://github.com/KeerthanaTV06/Liqufi-Hackathon",
    },
)