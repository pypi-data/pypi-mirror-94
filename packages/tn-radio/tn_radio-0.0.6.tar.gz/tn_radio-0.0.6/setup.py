import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tn_radio", # Replace with your own username
    version="0.0.6",
    author="THAVASIGTI",
    author_email="ganeshanthavasigti1032000@gmail.com",
    description="Tamil Nadu Local Online Fm Station",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/THAVASIGTI/tn_radio.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=["python-vlc"]
)