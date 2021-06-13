from setuptools import setup
from pathlib import Path

PARENT_DIR = Path().cwd()
README_PATH = PARENT_DIR.joinpath("README.md")

with README_PATH.open() as f:
    README = f.read()

setup(
    name="slack_handler",
    version="0.2.4",
    description="Python tool to extract File slacks from disk images.",
    url="https://github.com/Sim4n6/Slack_handler",
    long_description=README,
    long_description_content_type="text/markdown",
    author="ALJI Mohamed",
    author_email="sim4n6@gmail.com",
    license="GNU General Public License v2.0",
    packages=["slack_handler"],
    install_requires=["pytsk3", "libewf-python"],
    entry_points={
        "console_scripts": [
            "slack_handler=slack_handler.__main__:main",
        ]
    },
)
