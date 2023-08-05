import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dgbpy-dm',
    version='0.1.1',
    author='David Markus',
    author_email='david.datascientist@outlook.com',
    description='Useful dgb stuff.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='http://opendtect.com',
    packages=setuptools.find_packages(),
    install_requires=[
        "bokeh>=2.1.0",
        "psutil>=5.8.0",
        "h5py>=3.1.0",
        "joblib>=1.0.0",
        "sklearn>=0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)