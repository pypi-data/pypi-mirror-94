import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SORNSim",
    version="0.2.0",
    author="Marius Vieth",
    author_email="mv15go@gmail.com",
    description="Self Organizing Network Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitmv/Self-Organizing-Recurrent-Network-Simulator",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'PyQt5', 'pyqtgraph>=0.11.0rc0', 'matplotlib', 'scipy', 'scikit-learn', 'imageio', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)