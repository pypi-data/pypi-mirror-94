import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stsmd", # Replace with your own username
    version="0.0.1",
    author="Alice Petit, Nolwenn Sourice",
    author_email="nolwennsourice@gmail.com",
    description="A small package to get closest text document with SMD and Sentence transformers embeddings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)