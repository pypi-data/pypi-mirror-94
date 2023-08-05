from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'Python package for simulation of grain-based system'
LONG_DESCRIPTION = 'Python package for simulation of grain-based system using molecular dynamics method and agent-based model'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="butiran", 
        version=VERSION,
        author="Sparisoma Viridi",
        author_email="<dudung@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
				url="https://github.com/dudung/butiran",
				
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
