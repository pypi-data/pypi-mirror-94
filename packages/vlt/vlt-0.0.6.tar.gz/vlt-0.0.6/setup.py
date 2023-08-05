from setuptools import setup, find_packages

def read_requirements(requirements_file_path):
    """Return dependencies from a requirements file as a list.

    Read a requirements '.txt' file, where dependencies are separated by a new line.
    Removes all comments and options for pip, and return as a list of dependencies.

    :return:    requirements
    :rtype:     list
    """
    with open(requirements_file_path, 'r') as f:
        data = f.readlines()
    data = [i[: i.find("#")] if "#" in i else i for i in data]
    data = [i.strip() for i in data if i.strip()]
    data = [i for i in data if not i.startswith("-")]
    return data

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author="Michael Green",
    author_email="1mikegrn@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules" 
    ],
    description="a python-based password manager",
    entry_points={
        'console_scripts': ['vlt=vlt.app:main']
    }, 
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
    long_description=long_description,
    long_description_content_type = "text/markdown",
    name="vlt",
    packages=find_packages(where="src"),
    package_data={"": ['*.txt']},
    package_dir={"": "src"},   
    python_requires='>=3.6',
    tests_require=read_requirements("requirements_testing.txt"),
    url="https://github.com/1mikegrn/vlt",
    version="0.0.6",
)