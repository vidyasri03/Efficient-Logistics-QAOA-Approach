"""Setup configuration for Efficient Logistics Scheduling."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="efficient-logistics-qaoa",
    version="1.0.0",
    author="Your Team",
    author_email="your.email@example.com",
    description="Supply chain optimization using classical and quantum methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/efficient-logistics-qaoa",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
)
