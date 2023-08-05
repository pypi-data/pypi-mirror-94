import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open('requirements.txt', 'r', encoding='utf-8') as file:
    requirements = file.read().splitlines()

with open('VERSION.txt', 'r', encoding='utf-8') as file:
    version = file.read().strip()

setuptools.setup(
    name="pornhubSpider",
    version=version,
    author="ZoinkCN",
    author_email="zoinkcn@outlook.com",
    description="A simple spider of Pornhub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZoinkCN/pornhubSpider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=requirements
)
