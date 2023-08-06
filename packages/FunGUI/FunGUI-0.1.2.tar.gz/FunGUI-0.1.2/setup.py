import setuptools
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)
print(setuptools.find_packages())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FunGUI", # Replace with your own username
    version="0.1.2",
    author="shawn yan wang",
    author_email="shawnyanwang@gmail.com",
    description="It is a tool to easily generate GUI from a function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/shawnyanwang/fun_-gui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'FunGUI': ['title.png','test.fgui','FunGUI.pyw']},
    install_requires=[
        'matplotlib>=3.1.0',
        'pywin32>=223'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    python_requires='>=3.6',
)
