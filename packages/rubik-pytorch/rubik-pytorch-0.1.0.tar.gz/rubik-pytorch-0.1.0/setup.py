import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rubik-pytorch", 
    version="0.1.0",
    author="Jimin Tan",
    author_email="tanjimin@nyu.edu",
    description="Highly customizable Deep Learning training framework \
        base on PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tanjimin/rubik",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
