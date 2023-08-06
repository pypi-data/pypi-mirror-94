import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myimage",  # Replace with your own username
    version="0.1.1",
    author="MarkShawn2020",
    author_email="shawninjuly@gmail.com",
    description="A handful module for uploading local image and then get the path from specific server, "
                "especially good for those writing markdown journals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarkShawn2020/myimage",
    packages=setuptools.find_packages(
        exclude=['*.settings', ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        "requests",
        "qiniu",
    ],
)