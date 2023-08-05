# Zoom Toolkit


This is a simple yet useful toolkit implemented for working on zoom records. There exists 3 functionalities that 
 automates the video processing procedure designed specifically for Zoom videos.

## Features

 - Silence Cut
    - Detecting and eliminating high amount and long duration silent parts in videos.
 - Face Removal
     - Automatically detects and blurs the portrait of the speaker that shares screen.
 - Scene Detect
    - Detects important frames.

## Installation

Download the source code from <a href="https://github.com/OnurArdaB/Zoom-Toolkit/">here</a> and then just type the command below inside the project folder.

```.sh
python setup.py install
```

## Quick Start Guide

- Face Removal

```python
from zoom_toolkit.face_removal.face_remove import face_remove
face_remove("path to the file",False,1000,1050)
```

Module also allows users to state manual time zones for face removal with blurring or darkening option.

Further documentations will be announced soon.

This project has been developed under the supervision of Berrin Yanıkoğlu for ENS-492 (Graduation Project).
