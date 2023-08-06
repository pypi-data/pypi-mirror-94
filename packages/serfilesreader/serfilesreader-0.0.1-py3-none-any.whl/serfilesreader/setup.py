from setuptools import setup

setup(name="serfilesreader",
      version="0.0.1",
      description="A library handling SER files",
      long_description = file: README.md
      long_description_content_type ='text/markdown'
      author="JB BUTET",
      author_email="ashashiwa@gmail.com",
      packages=["serfilesreader"],
      install_requires=["opencv-python", "numpy", "astropy"],
      url="https://gitlab.com/ashashiwa/pyserfilesreader",
      license="LGPL 3.0")

