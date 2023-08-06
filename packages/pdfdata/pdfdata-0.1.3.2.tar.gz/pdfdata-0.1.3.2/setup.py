from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='pdfdata',
   version='0.1.3.2',
   description='Extracting text and data from PDFs',
   license="MIT",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Peter Meissner',
   author_email='retep.meissner@gmail.com',
   url="https://github.com/petermeissner/pdfdata",
   packages=['pdfdata'],  # same as name
   install_requires=[
     "PyMuPDF"
   ],  # external packages as dependencies
   scripts=[],
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
   ],
   python_requires='>=3.6'
)
