import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connection-notifier-nnrepos",
    version="0.1a",
    author="NN",
    description="a script that checks the host's data connection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NNRepos/connection_alerter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    entry_points={
        'console_scripts': ['notifier=notifier:main_loop']
    },
)
