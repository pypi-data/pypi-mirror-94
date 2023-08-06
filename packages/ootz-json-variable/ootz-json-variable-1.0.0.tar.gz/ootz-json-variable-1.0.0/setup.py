import setuptools


setuptools.setup(
    name="ootz-json-variable",
    version="1.0.0",
    license='MIT',
    author="oneofthezombies",
    author_email="hunhoekim@gmail.com",
    description="json variable using json pointer.",
    long_description=open('README.md').read(),
    url="https://github.com/oneofthezombies/json-variable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['jsonpointer==2.0'
    ],
)
