import setuptools

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logicplum",
    version="0.1.3",
    author="LogicPlum",
    author_email="message@logicplum.com",
    description="This client library is designed to support the LogicPlum API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LogicPlum/logicplum_v2",
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points={
            'console_scripts': [
                'logicplum = logicplum.logicplum:main'
            ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Operating System :: Developers/Data Scientists",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords='logicplum machine-learning AI automl prediction model',
    install_requires=requirements,
    python_requires='>=3.6',
)
