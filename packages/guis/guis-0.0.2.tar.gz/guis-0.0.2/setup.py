from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='guis',
    version='0.0.2',
    description='''This module is called GUIS which means GUI Simplified / Graphial User Interface Simplified.
                This module helps you in making your Tkinter GUI, Fast and Easy, and our module doesn't need .pack at the end :O''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["guis"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        ],
        url="https://github.com/Coding-bros/GUIS",
        author="Karthik",
        author_email="bkp.karthi@gmail.com",)
