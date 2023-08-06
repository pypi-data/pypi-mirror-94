import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dtleads-api-helper",
    version="0.0.2",
    author="Graham Ormond",
    author_email="graham@danieltimothyleads.com",
    description="A small Python package to assist with Daniel Timothy Leads API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Daniel-Timothy-Leads/dtleads-api-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)