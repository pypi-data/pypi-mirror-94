from setuptools import setup

setup(
    name="stsb3",
    version="0.1.0",
    description="Structural time series building blocks",
    url="https://gitlab.com/daviddewhurst/stsb3",
    author="David Dewhurst",
    author_email="drd@davidrushingdewhurst.com",
    license="MIT",
    packages=["stsb3"],
    install_requires=[
        "black",
        "numpy",
        "opt-einsum",
        "pyflakes",
        "pyro-api",
        "pyro-ppl",
        "pytest",
        "torch",
        "virtualenv",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
