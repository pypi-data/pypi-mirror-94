import setuptools
from setuptools import setup 

# reading long description from file 
with open('README.md') as file: 
	long_description = file.read() 


# specify requirements of your package here 
REQUIREMENTS = ['ephem','wikipedia','pyttsx3','datetime','pyperclip','translate'] 

# some more details 
CLASSIFIERS = [ 
	'Development Status :: 4 - Beta', 
	'Intended Audience :: Developers', 
	'Topic :: Internet', 
	'License :: OSI Approved :: MIT License', 
	'Programming Language :: Python', 
	'Programming Language :: Python :: 3', 
	'Programming Language :: Python :: 3.3', 
	'Programming Language :: Python :: 3.4', 
	'Programming Language :: Python :: 3.5', 
	] 

setuptools.setup(
    name="panclus", 
    version="2.6.0",
    author="Ayush Moghe",
    author_email="mogheayushgr8@gmail.com",
    description="PanclusGz is the upgraded version of panclus with multiple modules and more features + more useful in Ai building.PanclusGz is the best module for getting the weather forcast of any place in a single line of code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ayush2007A/PanclusGz",
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
)

