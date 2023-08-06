import pathlib

from setuptools import setup, find_packages  # type: ignore

requires = [
    "click",
    "boto3",
    "boto3-stubs[s3]",
]
test_requires = [
    "pytest",
    "moto",
]
readme = open(pathlib.Path(__file__).parent.resolve() / "README.rst").read()

setup(
    name="mr.s3",
    version="1.0.0b3",
    description="Syncing scripts Plone data between local and AWS S3",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Plone",
    ],
    author="Peacock",
    author_email="contact@peacock0803sz.com",
    url="https://github.com/peacock0803sz/mr.s3",
    keywords="Plone Python AWS",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={"tests": test_requires},
    entry_points="""\
    [console_scripts]
    mr.s3 = mr_s3.router:cli
    """,
)
