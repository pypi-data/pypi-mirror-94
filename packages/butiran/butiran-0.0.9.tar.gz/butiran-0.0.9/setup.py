from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'Python package for simulation of grain-based system'

# url https://www.freecodecamp.org/news/build-your-first-python-package/ [20210206]
# LONG_DESCRIPTION = 'Python package for simulation of grain-based system using molecular dynamics method and agent-based model'

# url https://packaging.python.org/guides/making-a-pypi-friendly-readme/ [20210207]
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()



# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="butiran", 
        version=VERSION,
        author="Sparisoma Viridi",
        author_email="<dudung@email.com>",
        description=DESCRIPTION,
        
				#long_description=LONG_DESCRIPTION,
        long_description=long_description,
				long_description_content_type='text/markdown',
				
				packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
				url="https://github.com/dudung/butiran-py",
				
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
