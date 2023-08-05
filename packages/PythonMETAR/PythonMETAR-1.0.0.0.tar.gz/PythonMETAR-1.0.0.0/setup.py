import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonMETAR", # Replace with your own username
    version="1.0.0.0",
    author="Matthieu BOUCHET",
    author_email="matthieu.bouchet@outlook.com",
    description="METAR Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatthieuBOUCHET/PythonMETAR",
    packages=['PythonMETAR'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)