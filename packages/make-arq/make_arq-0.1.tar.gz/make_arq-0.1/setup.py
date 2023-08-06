import numpy
from setuptools import Extension, setup

setup(
    name="make_arq",
    version="0.1",
    url="https://github.com/ickc/make_arq",
    author="Kolen Cheung",
    author_email="christian.kolen@gmail.com",
    license="GPL-3.0-only",
    keywords="Sony ARQ Fujifilm GFX 100",
    description="A tool for generating Sony A7RIII/IV and Fujifilm GFX 100 Pixel-Shift files.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        "numpy >=1.10,<2",
        "tifffile",
    ],
    extras_require={
        "extras": ["rawpy"]
    },
    packages=["make_arq"],
    package_dir={"make_arq": "src/make_arq"},
    ext_modules=[
        Extension(
            "_makearq", ["src/make_arq/_makearq.c"], include_dirs=[numpy.get_include()]
        )
    ],
    entry_points={
        "console_scripts": [
            "make_arq = make_arq.make_arq:main",
        ],
    },
)
