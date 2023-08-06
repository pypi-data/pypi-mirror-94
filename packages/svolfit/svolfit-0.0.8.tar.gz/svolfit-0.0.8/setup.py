import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svolfit",
    version="0.0.8",
    author="Michael A. Clayton Consulting Inc.",
    author_email="michael.clayton@sympatico.ca",
    description="Stochastic volatility models fit to historical time-series data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://currently.not.available",
#recall that for this to find somethign there needs to be an __init__.py in the directory:
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Development Status :: 3 - Alpha",
    ],
    keywords='stochastic volatility',
    python_requires='>=3.7',
    install_requires=[
   'numpy>=1.19,!=1.19.4',
   'pandas>=1.1',
   'scipy>=1.5'
    ]
)
