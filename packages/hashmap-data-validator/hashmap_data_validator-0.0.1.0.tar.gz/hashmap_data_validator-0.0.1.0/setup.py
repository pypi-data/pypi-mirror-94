import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hashmap_data_validator",
    version="0.0.1.0",
    author="Hashmap, Inc",
    author_email="accelerators@hashmapinc.com",
    description="A Python Package designed to validate data sources and sinks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hashmapinc/ctso/accelerators/data-engineering/hashmap_data_suite/hashmap-data-validator",
    packages=setuptools.find_packages(),
    package_data={
        "hdv": ["configurations/default_hdv_profiles.yml",
                "configurations/default_hdv_config.yml"]
    },
    install_requires=[
        'pyarrow==0.17.1',
        'pandas==1.1.4',
        'pyyaml==5.3.1',
        'snowflake-connector-python==2.3.6',
        'great-expectations==0.13.6',
        'json2html==1.3.0',
        'cx-Oracle==8.1.0',
        'SQLAlchemy==1.3.20',
        'providah==0.1.15.0',
        'click==7.1.2',
    ],
    entry_points={
        'console_scripts': [
            'hdv validate = hdv.cli_validator:cli_validate'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.7',
)