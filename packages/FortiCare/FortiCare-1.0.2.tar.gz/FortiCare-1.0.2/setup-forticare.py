import setuptools

with open("FortiCare/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

setuptools.setup(
    name="FortiCare",
    version=version,
    author="See \"Authors\" section",
    author_email="",
    description="FortiCare management package for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/FortiCare/",
    packages=["FortiCare"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires='>=3.6',
    install_requires=[
       'requests',
       'python-dateutil',
       'PyPDF2',
       'tabulate',
       'filelock',
       'validators'
   ]
)

#  python3 setup.py sdist bdist_wheel
