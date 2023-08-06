import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

install_requires = []
with open("requirements.txt") as file_obj:
    for req in file_obj:
        if req:
            install_requires.append(req)

tests_require = ["nose", "twine"]

packages = setuptools.find_packages()

setuptools.setup(
    name="nubium-utils",
    version="0.17.0",
    author="Edward Brennan",
    author_email="ebrennan@redhat.com",
    description="Some Kafka utility functions and patterns for the nubium project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.corp.redhat.com/mkt-ops-de/nubium-utils.git",
    packages=packages,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"dev": tests_require},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
