import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kirisearch",
    version="0.0.1",
    author="Kiri OÜ",
    author_email="hello@kiri.ai",
    description="Kiri Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kiri-ai/kiri-search",
    packages=setuptools.find_packages(),
    install_requires=[
        "transformers",
        "sentence_transformers",
        "nltk",
        "scipy",
        "shortuuid",
        "elasticsearch",
        "torch"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
