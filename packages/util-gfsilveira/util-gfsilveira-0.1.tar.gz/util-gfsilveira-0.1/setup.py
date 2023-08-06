import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="util-gfsilveira",
    version="0.1",
    author="GGuilherme F. Silveira",
    author_email="gfsilveira@gmail.com",
    description="Diverse and useful functions for various actions.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gfsilveira/meus_util.git",
    packages=['util'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)