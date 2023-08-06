import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multiprogramming", # Replace with your own username
    version="0.0.1",
    author="Siyuan Niu",
    author_email="siyuan.niu@lirmm.fr",
    description="A package for multiprogramming algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peachnuts/Multiprogramming",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "qiskit",
        "networkx",
    ],  # Optional
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)