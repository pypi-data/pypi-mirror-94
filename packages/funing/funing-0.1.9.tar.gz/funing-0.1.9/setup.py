import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="funing",
    version="0.1.9",
    author="larryw3i",
    author_email="larryw3i@163.com",
    description="A face recognition gui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larryw3i/Funing",
    scripts=['funing.py','setting.py'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)