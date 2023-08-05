import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ProtoDriver",
    version="0.0.2a1",
    author="ZynosStudios",
    author_email="zynosstudios@gmail.com",
    description="A simple Raspberry Pi web api for driving a MAX7219 dot matrix display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZynosStudios/ProtoDriverPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Other",
    ],
    python_requires='>=3.6, <3.8',
    install_requires=[
        "luma.led-matrix",
        "flask",
        "flask-restful",
        "pillow"
    ]
)
