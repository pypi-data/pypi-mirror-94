from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="msglite",
    version="0.29.1",
    description="Extracts emails and attachments saved in Microsoft Outlook's .msg files",  # noqa
    url="https://github.com/alephdata/msglite",
    author="OCCRP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL",
    packages=["msglite"],
    py_modules=["msglite"],
    include_package_data=True,
    install_requires=[
        "olefile>=0.46",
        "ebcdic>=1.1.1",
        "chardet",
        "pytz",
    ],
)
