import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent.parent
print (HERE)

# The text of the README file
README = (HERE / "README.txt").read_text()
#print (README)

# This call to setup() does all the work
setup(
    name="hashbrown",
    #versioning stuff
    version="4.0",
    description="Read the documentation on Github at https://github.com/iamchoking/Hashbrown",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/iamchoking/Hashbrown",
    author="Hyungho Choi",
    author_email="planner.king@gmail.com",
    classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    ],
    #license="MIT",
    packages = find_packages(),
    install_requires=["openpyxl", "matplotlib"],
    include_package_data=True
)
'''

install_requires=["feedparser", "html2text"],
entry_points={
    "console_scripts": [
        "realpython=reader.__main__:main",
    ]
},
'''