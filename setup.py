"""Based off of pypa/sampleproject
https://raw.githubusercontent.com/pypa/sampleproject/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="sisou",  # Required
    version="1.0.0",  # Required
    description="A powerful tool to conveniently update all of your ISO files!",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional
    url="https://github.com/JoshuaVandaele/SuperISOUpdater",  # Optional
    author="Joshua Vandaele",  # Optional
    author_email="joshua@vandaele.software",  # Optional
    classifiers=[  # Optional
        # https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="ventoy, updater, os, iso, updater, sisou, cli",  # Optional
    # package_dir={"superisoupdater": "."},  # Optional
    packages=find_packages(),  # Required
    py_modules=["sisou"],  # Required
    python_requires=">=3.10, <4",
    install_requires=[
        "beautifulsoup4==4.12.2",
        "requests==2.31.0",
        "tqdm==4.65.0",
        "PGPy==0.6.0",
    ],  # Optional
    # extras_require={
    #     "dev": [""],
    #     "test": [""],
    # },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={  # Optional
    #     "sample": ["package_data.dat"],
    # },
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        "console_scripts": [
            "sisou = sisou:main",
        ],
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/JoshuaVandaele/SuperISOUpdater/issues",
        "Source": "https://github.com/JoshuaVandaele/SuperISOUpdater/",
    },
)
