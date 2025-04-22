from setuptools import setup, find_packages

setup(
    name="EventManagerPy",
    version="0.2.8",
    author="Botan Celik",
    author_email="botan.celik@icloud.com",
    description="EventManager is a logging module designed to be used in a multi-threaded environment",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheBloodyAmateur/EventManagerPython",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "setuptools~=78.1.0",
        "psutil~=7.0.0",
        "pydantic~=2.11.3",
        "atomics~=1.0.3",
        "urllib3~=2.4.0",
    ],
)
