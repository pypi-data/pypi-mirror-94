#MY FIRST PYTHON PACKAGE
import setuptools

from music_analysis import __about__


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='music_analysis_noha',  # Replace with your own username e.g example-pkg-name #TODO
    version=__about__.__version__,  # TODO
    author='Noha',
    author_email='noahalsultan@gmail.com',  # TODO
    description='A small example of package',  # TODO
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',  # TODO
    license=license,
    packages=setuptools.find_packages(exclude=('tests*', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
    python_requires='>=3.6',
)