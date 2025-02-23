from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='AI-Adventure-RPG',
    version='1',
    packages=['AI-Adventure-RPG'],
    url='https://github.com/RenathaPutri/AI-Adventure-RPG',
    license='MIT',
    author='Renatha Putri',
    author_email='queennatha444@gmail.com',
    description='This package contains implementation of an adventure RPG on command-line interface with Google Gemini AI integrated into it.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "AI-Adventure-RPG=AI-Adventure-RPG.AI-Adventure-RPG:main",
        ]
    }
)