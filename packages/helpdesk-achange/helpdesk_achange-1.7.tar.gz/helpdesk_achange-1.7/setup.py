import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helpdesk_achange",
    version="1.7",
    author="alireza",
    author_email="alirezaghaempanah2015@gmail.com",
    include_package_data=True,
    description="ticketing project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/django3-helpdesk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)