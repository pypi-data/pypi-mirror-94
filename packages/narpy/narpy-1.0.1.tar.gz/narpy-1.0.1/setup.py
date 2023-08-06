from distutils.core import setup

setup(
    # Application name:
    name="narpy",

    # Version number (initial):
    version="1.0.1",

    # Application author details:
    author="Jago Strong-Wright",
    author_email="jagoosw@protonmail.com",

    # Packages
    packages=["narpy"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/jagoosw/narpy/",

    #
    license="LICENSE.txt",
    description="A simple NASA AMES file Reader for Python",

    long_description="""narpy is a simple NASA AMES file Reader for Python. There didn't seem to be any functioning libraries for opening .na or NASA AMES files in Python so this is what I ended up with. Functionality is fairly limited but gets the core needs done.
    
    Please see the "Homepage" for more details as the markdown wouldn't render here """,

    # Dependent packages (distributions)
    install_requires=[
        "numpy",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: Markdown"
    ],
)