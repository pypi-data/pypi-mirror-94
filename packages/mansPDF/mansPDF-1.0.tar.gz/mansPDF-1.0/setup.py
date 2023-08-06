import setuptools
from pathlib import Path
setuptools.setup(
    name="mansPDF",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # exclude shiis diras, jo tur ir source code
    packages=setuptools.find_packages(exclude=["test", "data"])

)
