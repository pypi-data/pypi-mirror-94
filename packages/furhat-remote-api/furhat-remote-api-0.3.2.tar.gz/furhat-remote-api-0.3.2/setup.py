from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="furhat-remote-api",
    version="0.3.2",
    install_requires=[
            "certifi>=2017.4.17",
            "python-dateutil>=2.1",
            "six>=1.10",
            "urllib3>=1.23"
        ],
    description="Furhat Remote API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.furhat.io/remote-api",
    packages=find_packages(),
    include_package_data=True,
    author="Furhat Robotics",
    author_email="support@furhatrobotics.com"
)