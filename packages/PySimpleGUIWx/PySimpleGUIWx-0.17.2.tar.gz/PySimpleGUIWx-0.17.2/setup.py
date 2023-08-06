import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="PySimpleGUIWx",
    version="0.17.2",
    author="MikeTheWatchGuy",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="The Engineering Pre-Release WxPython version of PySimpleGUI. PySimpleGUI SDK Launched in 2018 Actively developed and supported. Super-simple to create custom GUI's.  Now supports tkinter, Qt, WxPython, and Remi",
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=['WxPython', ],
    keywords="GUI UI tkinter wrapper simple easy beginner novice student graphics progressbar progressmeter",
    url="https://github.com/PySimpleGUI/PySimpleGUI",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ),
)