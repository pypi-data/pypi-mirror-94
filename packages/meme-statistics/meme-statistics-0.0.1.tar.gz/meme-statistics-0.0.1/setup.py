from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="meme-statistics",
    version="0.0.1",
    author="Himanshu Ramchandani",
    author_email="himanshuramchandani08@gmail.com",
    description="A package with all Statistical measures and models from scratch.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/HemansAI/meme-statistics",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
)