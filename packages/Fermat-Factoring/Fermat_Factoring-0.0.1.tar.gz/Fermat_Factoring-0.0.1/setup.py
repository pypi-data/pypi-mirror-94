import setuptools

with open("README.md", "r")as fh:
    long_description = fh.read()

setuptools.setup(
    name="Fermat_Factoring",
    version="0.0.1",
    author="Mihir Goyenka",
    author_email="mihirgoyenka@gmail.com",
    description="Factorising integers based on Fermat's technique",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mihirgit/Fermat_Factoring",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)