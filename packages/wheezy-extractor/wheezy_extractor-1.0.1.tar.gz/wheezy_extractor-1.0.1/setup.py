from setuptools import setup, find_packages
setup(
    name="wheezy_extractor",
    version="1.0.1",
    description="Babel extracto for Wheezy templates",
    url="https://github.com/Polsaker/wheezy_extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    entry_points="""
    [babel.extractors]
    wheezyhtml = wheezy_extractor:extract_wheezy
    """
)
