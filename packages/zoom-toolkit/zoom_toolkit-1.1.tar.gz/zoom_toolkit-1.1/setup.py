from setuptools import setup, find_packages

setup(
   name='zoom_toolkit',
   version='1.1',
   description='This is a simple yet useful toolkit implemented for working on zoom records.',
   license="MIT",
   url='https://github.com/OnurArdaB/Zoom-Toolkit',
    download_url = 'https://github.com/OnurArdaB/Zoom-Toolkit/archive/v_01.tar.gz',    # I explain this later on
   author='Onur Arda Bodur',
   author_email='onurarda@sabanciuniv.edu',
   packages=['zoom_toolkit'],  
   install_requires=['opencv-python', 'moviepy'], #external packages as dependencies
   classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
)