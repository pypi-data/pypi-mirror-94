import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googlepy", # Replace with your own username
    version="0.0.3",
    scripts=['googlepy'],
    author="Sakurai07",
    author_email="blzzardst0rm@Gmail.com",
    description="Google.py is a cli client of google written in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sakurai07/google.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
