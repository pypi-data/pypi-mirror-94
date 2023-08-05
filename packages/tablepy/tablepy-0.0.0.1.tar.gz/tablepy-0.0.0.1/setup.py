from setuptools import setup, find_packages

setup(
    name = "tablepy",
    packages=["tablepy"],
    version="0.0.0.1",
    license='wtfpl',
    description="table generator for python",
    long_description="""
        tablepy is a python package that can be used to generate tables 
    """,
    include_package_data = True,
    author = 'Julian Wandhoven',                   # Type in your name
    author_email = 'julian.wandhoven@fgz.ch',

    url="https://github.com/JulianWww/tables",
    project_urls={
        "documentation": "https://tablepy.readthedocs.io/en/latest/index.html"
    },
    keywords=["tables","rendering"],
    classifiers=[
    'Development Status :: 2 - Pre-Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6' ,
    'Programming Language :: Python :: 3'],#Specify which pyhton versions that you want to support
)
