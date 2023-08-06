import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InowasFlopyAdapter",
    version="1.4.0",
    author="Ralf Junghanns",
    author_email="ralf.junghanns@gmail.com",
    description="A FLOPY wrapper for the INOWAS-platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inowas/InowasFlopyAdapter",
    packages=setuptools.find_packages(),
    install_requires=[
        'flopy==3.3.2',
        'geojson>=2.5',
        'nose>=1.3',
        'numpy>=1.9',
        'pyproj>=2.6',
        'rasterio>=1.1',
        'scipy>=1.4',
        'shapely>=1.7',
        'sklearn>=0.0',
        'setuptools>=50.0',
        'twine>=3.2',
        'utm>=0.5.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
