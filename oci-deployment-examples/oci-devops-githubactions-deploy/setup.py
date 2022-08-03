from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="fastapp",
    version="0.0.1",
    author="Rahul MR",
    author_email="",
    description="Sample fastapi python app",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/RahulMR42/oci_tf_exercise",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
