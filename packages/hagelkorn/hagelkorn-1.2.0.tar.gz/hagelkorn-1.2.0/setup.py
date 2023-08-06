from setuptools import setup

__packagename__ = "hagelkorn"


def get_version():
    import os
    import re

    VERSIONFILE = os.path.join(__packagename__, "__init__.py")
    initfile_lines = open(VERSIONFILE, "rt").readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError(f"Unable to find version string in {VERSIONFILE}.")


__version__ = get_version()


setup(
    name=__packagename__,
    packages=[__packagename__],  # this must be the same as the name above
    version=__version__,
    description="Implements an algorithm to generate alphanumeric IDs that increase monotonically with time.",
    url="https://github.com/michaelosthege/hagelkorn",
    download_url="https://github.com/michaelosthege/hagelkorn/tarball/%s" % __version__,
    author="Michael Osthege",
    author_email="m.osthege@fz-juelich.de",
    copyright="(c) 2018 Forschungszentrum Jülich GmbH",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
    ],
    install_requires=[],
)
