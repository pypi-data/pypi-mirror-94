import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docwmd", # Replace with your own username
    version="0.0.6",
    author="Alice Petit, Nolwenn Sourice",
    description="A small package using wmd to get closet doc to a chosen doc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/guillaume.burgaud.name/smd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)