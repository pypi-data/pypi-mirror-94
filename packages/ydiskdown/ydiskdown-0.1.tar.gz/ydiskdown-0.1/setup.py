import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ydiskdown", # Replace with your own username
    version="0.1",
    author="IamSVP",
    author_email="PSV1994@yandex.ru",
    description="Simple Yandex Disk downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IamSVP94/ydown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
