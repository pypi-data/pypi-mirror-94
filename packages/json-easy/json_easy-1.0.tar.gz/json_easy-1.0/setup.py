from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='json_easy',
    version='1.0',
    description='Json DB\'s made easy',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ConnorTippets/json-easy/',
    author='meiscool466',
    license='MIT',
    packages=["json_easy"],
    python_requires=">=3.8",
    keywords=["json", "db", "easy"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        
    ],
)
