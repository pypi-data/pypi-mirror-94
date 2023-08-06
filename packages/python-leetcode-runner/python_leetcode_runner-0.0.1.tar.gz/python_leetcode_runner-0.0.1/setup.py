import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_leetcode_runner",
    version="0.0.1",
    author="Tushar Sadhwani",
    author_email="tushar.sadhwani000@gmail.com",
    description="A CLI app to run any given Leetcode python solution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tusharsadhwani/python_leetcode_runner",
    py_modules=['leetcode'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['pyleet=leetcode:pyleet'],
    }
)
