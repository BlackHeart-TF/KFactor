# setup.py
from setuptools import setup, find_packages

setup(
    name="KFactor",
    version="0.4",
    python_requires='>=3.10',
    packages=find_packages(),
    entry_points={
        "gui_scripts": [
            "kfactor=kfactor.main:main",
        ],
    },
)
