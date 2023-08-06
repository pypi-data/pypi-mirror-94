"""
    This is the setup file for the PIP minecraft_learns package.

    Written By: Kathryn Lecha and Nathan Nesbitt
    Date: 2021-02-02
"""

from setuptools import setup

setup(
    name="minecraft_stores",
    version="0.0.1",
    description=
        "library for saving minecraft game data to disk.",
    url="https://github.com/Nathan-Nesbitt/Minecraft_Store",
    author=(
        "Carlos Rueda Carrasco, Kathryn Lecha, Nathan Nesbitt, " + 
        "Adrian Morillo Quiroga"),
    packages=[
        "minecraft_stores"
    ],
    install_requires=[
        "pandas",
        "wheel",
        "nest_asyncio",
        "pytest-asyncio",
        "pytest"
    ],
    zip_safe=False
)
