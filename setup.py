import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connection-notifier-nnrepos",
    version="0.1rc4",
    author="NN",
    description="a script that checks the host's data connection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NNRepos/connection_alerter",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyttsx>=1.1",
        "speedtest-cli>=2.1.2",
        "matplotlib>=2.2.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': ['notifier=connection_notifier.notifier:main_loop']
    },
)
