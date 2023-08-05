import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_sec_log", # Replace with your own username
    version="0.1.1.2.6",
    author="TechSmit",
    author_email="techsmithacker@gmail.com",
    description="Python Package For Login Verification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PythonProgramme/Python-Code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
