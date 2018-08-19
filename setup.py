import setuptools

with open("README.md", "r") as mysetup:
    long_description = mysetup.read()

setuptools.setup(
    name="pedvcfsim",
    version="1.0.1",
    author="Isaac Akogwu",
    author_email="isaac.akogwu@gmail.com",
    description="A package to simulate Variant Call Format (VCF) file from pedigree or graph like data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AisaacO/pedvcfsim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
		"Development Status :: 4 - Beta",
    ],
)
