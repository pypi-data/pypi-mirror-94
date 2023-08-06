import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geizhalscrawler",
    version="0.1",
    setup_requires=['setuptools_scm'],
    author="Timo Herrmann",
    author_email="git@therr.de",
    install_requires=[
        'beautifulsoup4>=4.6.3',
        'requests>=2.19.1'
    ],
    description="A parser for the Geizhals.eu website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timherrm/geizhalscrawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
