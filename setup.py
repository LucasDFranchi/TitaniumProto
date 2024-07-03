from setuptools import setup, find_packages

setup(
    name="Titanium Proto",
    version="0.1.0",
    description="A Python library to generate C++ classes from JSON for working with structs.",
    author="Lucas D. Franchi",
    author_email="LucasD.Franchi@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # Add any dependencies here if required
    ],
    entry_points={
        'console_scripts': [
            'titanium-proto = titanium_proto.titanium_proto:main',
            # Define command-line scripts here if applicable
        ],
    },
    extras_require={
        "dev": [
            "pytest >= 6.2.4",
            "pytest-cov >= 2.12.1",
            "coverage >= 5.5",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
