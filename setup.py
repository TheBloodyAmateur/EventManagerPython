from setuptools import setup, find_packages

setup(
    name="EventManagerPy",
    version="1.0.1",
    author="Botan Celik",
    author_email="botan.celik@icloud.com",
    description="EventManager is a logging module designed to be used in a multi-threaded environment",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheBloodyAmateur/EventManagerPython",
    packages=find_packages(),
    python_requires=">=3.13",
    install_requires=open("requirements.txt").read().splitlines()
)
