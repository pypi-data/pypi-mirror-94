import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='rdv-settings',
     version='9999.9999',
     scripts=['rendezvous'] ,
     author="X",
     author_email="chooqu7geb@protonmail.com",
     description="An utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
