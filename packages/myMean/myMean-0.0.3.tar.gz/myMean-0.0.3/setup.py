from setuptools import setup, find_packages

setup(
	name="myMean",
	version="0.0.3",
	author="Ani Chattaraj",
	packages=find_packages(),
	install_requires=['numpy'],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
	)
	