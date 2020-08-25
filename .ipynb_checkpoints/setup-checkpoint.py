import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="random_number_model",
    version="0.0.19",
    author="Avinash Joshi",
    author_email="akshay.ambekar@dominodatalab.com",
    description="A random number model",
    long_description="A model that returns a random number between a range",
    long_description_content_type="text/markdown",
    url="https://github.com/ddl-aambekar/model",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
