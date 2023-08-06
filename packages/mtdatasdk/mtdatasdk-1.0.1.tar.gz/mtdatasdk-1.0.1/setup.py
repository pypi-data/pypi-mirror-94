import os
import sys
import re
from setuptools import setup, find_packages


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def get_version():
    with open(os.path.join(THIS_FOLDER, 'mtdatasdk', '__init__.py'), "rb") as f:
        content = f.read().decode("utf-8")
        version = re.match(r".*__version__ = \"(.*?)\"",
                           content, re.S).group(1)
    return version


def get_long_description():
    with open(os.path.join(THIS_FOLDER, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
    return long_description


def _parse_requirement_file(path):
    if not os.path.isfile(path):
        return []
    with open(path) as f:
        requirements = [line.strip() for line in f if line.strip()]
    return requirements


def get_install_requires():
    if sys.version_info.major < 3:
        requirement_file = os.path.join(THIS_FOLDER, "requirements-py2.txt")
    else:
        requirement_file = os.path.join(THIS_FOLDER, "requirements.txt")
    return _parse_requirement_file(requirement_file)


setup(
    name="mtdatasdk",
    version=get_version(),
    description="mtdatasdk<easy utility for getting financial market data of China>",
    packages=find_packages(exclude=("tests", "tests.*")),
    author="zzb",
    author_email="bwyuchi@163.com",
    license='MIT License',
    package_data={'': ['*.*']},
    url="https://github.com/xjtu-quant/mtdatasdk",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=get_install_requires(),
    zip_safe=False,
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
