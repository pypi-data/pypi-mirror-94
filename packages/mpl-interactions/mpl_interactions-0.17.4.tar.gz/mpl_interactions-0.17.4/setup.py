from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# extract version
path = path.realpath("mpl_interactions/_version.py")
version_ns = {}
with open(path, encoding="utf8") as f:
    exec(f.read(), {}, version_ns)
version = version_ns["__version__"]

name = "mpl_interactions"

setup_args = dict(
    name=name,
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.3",
    ],
    author="Ian Hunt-Isaak",
    author_email="ianhuntisaak@gmail.com",
    license="BSD",
    platforms="Linux, Mac OS X, Windows",
    description="Matplotlib aware interact functions",
    keywords=["Jupyter", "Widgets", "IPython", "Matplotlib"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Jupyter",
        "Framework :: Matplotlib",
    ],
    url="https://github.com/ianhi/mpl-interactions",
    extras_require={
        "jupyter": [
            "ipywidgets>=7.5.0,<8",
            "ipympl>=0.5.8",
        ],
        "doc": [
            "sphinx>=1.5",
            "mock",
            "numpydoc",
            "recommonmark",
            "sphinx_rtd_theme",
            "nbsphinx",
            "jupyter_sphinx",
            "pytest_check_links",
            "pypandoc",
            "jupyter-sphinx",
            "sphinx-copybutton",
            "sphinx-autobuild",
            "xarray",
            "sphinx_gallery>=0.8.2",
            "mpl-playback>=0.1.1",
        ],
        "test": [
            "pytest",
            "pytest-mpl",
            "nbval",
            "PyQt5",
            "black",
            "pandas",
            "requests",
            "scipy",
            "xarray",
        ],
        "dev": [
            "pre-commit",
        ],
    },
)

if __name__ == "__main__":
    setup(**setup_args)
