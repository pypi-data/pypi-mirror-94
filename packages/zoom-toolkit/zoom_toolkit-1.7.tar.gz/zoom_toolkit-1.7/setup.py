from setuptools import setup, find_packages
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
   name='zoom_toolkit',
   version='1.7',
   description='This is a simple yet useful toolkit implemented for working on zoom records.',
   description_file="README.md",
    long_description=long_description,
    long_description_content_type='text/markdown',
   license="MIT",
   url='https://github.com/OnurArdaB/Zoom-Toolkit',
   download_url = 'https://github.com/OnurArdaB/Zoom-Toolkit/archive/v_01.tar.gz',    # I explain this later on
   keywords = ['Zoom','Automated','Video Processing'],
   author='Onur Arda Bodur',
   author_email='onurarda@sabanciuniv.edu',
   packages=['zoom_toolkit'],  
   install_requires=['opencv-python', 'moviepy','scipy','audiotsm','scenedetect'], #external packages as dependencies
   classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
)