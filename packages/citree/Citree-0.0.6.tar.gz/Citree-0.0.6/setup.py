#!/usr/bin/env python


# In[ ]:


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Citree", 
    version="0.0.6",
    author="Igor Mintz",
    author_email="igormintz@gmail.com",
    description="creates citation tree plot using DOI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igormintz/Citree",
    packages=["citree"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

