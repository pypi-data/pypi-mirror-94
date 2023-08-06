from pathlib import Path

from setuptools import setup, find_packages


def make_long_description():
    here = Path(__file__).parent
    readme = (here / "README.md").read_text()
    changelog = (here / "CHANGELOG.md").read_text()
    return f"{readme}\n\n{changelog}"


setup(
    name="py3status-portfolio",
    version="0.1",
    description="view stock portfolio",
    # long_description=make_long_description(),
    # long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    install_requires=["py3status>=3.20", "stockquotes"],
    package_dir={"": "src"},
    entry_points={"py3status": ["module = py3status_portfolio.portfolio"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

)
