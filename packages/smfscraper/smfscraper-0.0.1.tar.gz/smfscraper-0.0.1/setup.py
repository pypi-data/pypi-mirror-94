from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Wrapper for scraping simplemachineforums'
LONG_DESCRIPTION = 'Wrapper Library for scraping simplemachineforums with their main url only.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="smfscraper", 
        version=VERSION,
        author="Utsav Magar",
        author_email="utsavmagar88728@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests', 'beautifulsoup4'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package', 'smf', 'simplemachineforums', 'smfscraper', 'smfapi'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)