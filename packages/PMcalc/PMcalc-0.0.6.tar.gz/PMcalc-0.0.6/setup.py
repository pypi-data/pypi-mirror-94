import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PMcalc",
    version="0.0.6",
    author="Vsevolod Kabrits",
    author_email="seva.kabrits@gmail.com",
    description="Package for performing calculations with uncertainties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skabrits/smartcalc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)