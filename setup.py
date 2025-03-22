from setuptools import setup, find_packages

setup(
    name="etl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "arcgis",
        "python-dotenv",
        "requests",
        "python-dateutil"
    ],
    entry_points={
        "console_scripts": [
            "feature-layer-etl=etl.update_feature_layer:update_feature_layer"
        ]
    },
    author="Justin Guthrie",
    description="ETL pipeline to automatically update a feature layer into ArcGIS Online",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
