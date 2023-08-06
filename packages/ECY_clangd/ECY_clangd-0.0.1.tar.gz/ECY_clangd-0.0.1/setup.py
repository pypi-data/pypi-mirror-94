import setuptools
import sys

long_description = "Clone from https://github.com/clangd/clangd/releases/tag/11.0.0"

def GetCurrentOS():
    temp = sys.platform
    if temp == 'win32':
        return 'windows'
    if temp == 'darwin':
        return 'mac'
    return 'linux'


clangd_version = 'ECY_%s_clangd>=0.0.1' % (GetCurrentOS())

setuptools.setup(name="ECY_clangd",
                 version="0.0.1",
                 author="jimmy huang",
                 author_email="1902161621@qq.com",
                 description="clangd for ECY",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/clangd/clangd/releases/tag/11.0.0",
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License"
                 ],
                 install_requires=[clangd_version])
