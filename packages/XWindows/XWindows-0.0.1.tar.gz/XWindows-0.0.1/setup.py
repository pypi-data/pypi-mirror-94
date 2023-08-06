from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'X Server client to access windows and automate keypresses'
LONG_DESCRIPTION = '''It is created to provide features like getting specific window attributes 
    like height, width, co-ordinates, image of the window and automate keypresses all these 
    features without compromising speed and efficiency. Main intention is to provide support for
    opencv projects on linux to get specific window images and automate keyboard based on gestures etc,
 '''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="XWindows", 
        version=VERSION,
        author="sleepingsaint",
        author_email="suryasantosh14523@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["python-xlib"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python3', 'XServer', 'Opencv', 'linux'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
        ]
)