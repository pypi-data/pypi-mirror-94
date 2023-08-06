import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

excluded = ["howl_training*"]

setuptools.setup(
    name="howl",
    version="0.1.0",
    author="Anserini Gaggle",
    author_email="anserini.gaggle@gmail.com",
    description="A wake word detection toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/castorini/howl",
    install_requires=requirements,
    packages=setuptools.find_packages(exclude=excluded),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
