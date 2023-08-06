import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chess-heatmap", # Replace with your own username
    version="0.0.6.2",
    author="Sravanti Tatiraju",
    author_email="sravanti.p21@gmail.com",
    description="Package to generate chess heatmaps from pgn files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
