from setuptools import setup

def get_version():
    with open("VERSION", encoding='utf-8') as f:
        return f.read()

def get_requires():
    with open("requirements.txt", encoding='utf-8') as f:
        return f.read()

def get_readme():
    with open("README.md", encoding='utf-8') as f:
        return f.read()

def next_breakversion(s):
    n = int(s[0])
    return "{}.0.0".format(str(n+1))

def correctfmt(s):
    parts = s.split("==")
    name = parts[0]
    version = parts[1]
    limitop = ">={},<{}".format(version, next_breakversion(version))
    return "{}({})".format(name,limitop)

requirements = list(map(
    correctfmt,
    filter(lambda x: x != '', get_requires().split("\n"))
))

VERSION = get_version()

README = get_readme()

setup(
    name="makru",
    version=VERSION,
    description="A simple, readable way to compile your program",
    long_desciption=README,
    long_desciption_content_type="text/markdown",
    author="The Makru Contributors",
    url="https://gitlab.com/jinwa/makru",
    packages=['makru'],
    package_data={
        "makru": ["requirements.txt", "VERSION"]
    },
    entry_points="""
    [console_scripts]
    makru = makru.main:main
    """,
    install_requires=requirements
)
