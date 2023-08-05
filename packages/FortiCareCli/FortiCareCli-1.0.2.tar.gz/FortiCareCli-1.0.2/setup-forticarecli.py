import setuptools

with open("FortiCareCli/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

setuptools.setup(
    name="FortiCareCli",
    version=version,
	 scripts=["FortiCareCli/fccli", "FortiCareCli/fccli.py"],
    author="See \"Authors\" section",
    author_email="",
    description="Example application to interact with FortiCare library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/FortiCareCli/",
    packages=["FortiCareCli"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires='>=3.6',
    install_requires=[
       'FortiCare=='+version
   ]
)

#  python3 setup.py sdist bdist_wheel
