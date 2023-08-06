from setuptools import setup, find_packages

def read(rel_path):
    with open(rel_path, "r", encoding="utf-8") as fh:
        return fh.read()
def gv(rel_path, what):
    for line in read(rel_path).splitlines():
        if line.startswith(what):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find.")

setup(
    name=gv("emvcs/__init__.py", '__name__'),
    version=gv("emvcs/__init__.py", '__version__'),
    author="mstouk57g",
    author_email="mstouk57g@yeah.net",
    description="Email via-code sender.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://mstouk57g.github.io/emvcs/",
    project_urls={
        "Documentation": "https://github.com/mstouk57g/emvcs/blob/main/README.md",
        "Source": "https://github.com/mstouk57g/emvcs",
        "Changelog": "https://github.com/mstouk57g/emvcs/releases",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires='>=3.9.0',
)
