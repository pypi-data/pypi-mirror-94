import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harmonoid-module", # Replace with your own username
    version="1.0.0.2",
    author="harmonoid Team",
    description="Harmonoid-service wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harmonoid/harmonoid-module",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'ytmusicapi',
        'pytube',
        "mutagen",
        "aiofiles",
        "httpx"
    ],
    python_requires='>=3.6',
)
