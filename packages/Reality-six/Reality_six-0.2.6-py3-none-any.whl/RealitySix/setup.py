
des=open("RealitySix/README.md","r",encoding="utf-8")
long=des.read()
import setuptools
setuptools.setup(
    name="Reality-six", 
    version="0.2.6", 
    author="pkg_uploaders", 
    author_email="example@example.com", 
    description="A simple package that tells you reality.", 
    long_description=long,
    long_description_content_type="text/markdown",
    url="https://github.com/Hillo232/Reality/tree/main", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)