import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="qlikconnect",
 
    version="0.1.4",
 
    author="Ayush Dabral",
 
    author_email="ayushdabral88@gmail.com",
 
    description="A Python library to interact with Qliksense.",
 
    long_description=long_description,
 
    long_description_content_type="text/markdown",
    keywords= "qlik,qliksense,sense",
    url="https://github.com/001ayushdabral/qlikconnect",
    packages=setuptools.find_packages(),
 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
