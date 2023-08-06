import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="number_comparator",
    version="0.0.5",
    author="Diego Ramirez",
    author_email="dr01191115@gmail.com",
    description="A numeric comparator package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        'Topic :: Software Development :: Build Tools',
        'Topic :: Scientific/Engineering :: Mathematics',
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="numbers number comparations operations python",
    python_requires='>=3.7',
)
