import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dgbpy-dm',
    version='0.1.0',
    author='David Markus',
    author_email='david.datascientist@outlook.com',
    description='Useful dgb stuff.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='http://opendtect.com',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)