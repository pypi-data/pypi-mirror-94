import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="realtime3d",
    version="0.0.1",
    author="Andy Martin",
    author_email="andy.martin@schrodinger.com",
    description="realtime3d",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schrodinger/",
    packages=setuptools.find_packages(),
    classifiers=[],
)
