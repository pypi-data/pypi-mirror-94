import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="histodata",
    version="0.2.1",
    author="Jonas Annuscheit",
    author_email="Jonas.Annuscheit@htw-berlin.de",
    description="Histopathology datasets for PyTorch environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.tools.f4.htw-berlin.de/cbmi-charite/histodata",
    packages=setuptools.find_packages(
        exclude=(
            "examples",
            "tests",
        )
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "matplotlib",  # TODO specify version
        "numpy",  # TODO specify version
        "torch>=1.5.1",
        "torchvision>=0.6.1",
        "imagesize",
        "tiatoolbox",
        "opencv-python-headless",
    ],
)

