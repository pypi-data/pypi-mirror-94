"""Info for setup tools."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bronotes",
    version="1.7.1",
    author="j wizzle",
    author_email="info@hossel.net",
    description="A commandline note organization tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwizzle/bronotes",
    packages=setuptools.find_packages(),
    package_data={
        "bronotes": ["config.yml.sample"],
    },
    install_requires=[
        'pyyaml',
        'shtab',
        'pyperclip',
        'gitpython'
    ],
    entry_points={
        'console_scripts': [
            'bnote=bronotes:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
