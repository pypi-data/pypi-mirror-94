import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sftpConfigReader",
    version="1.0.0",
    author="Vitalija Alisauskaite (alv2017)",
    author_email="alv2017@protonmail.com",
    description="SFTP configuration reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alv2017/sftp_config_reader.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)