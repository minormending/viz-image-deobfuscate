# Viz Manga Unobfuscator

Viz manga pages are delivered to the browser as obfuscated images and the client JS is responsible for unobfuscating those images for the viewer to read. This program reproduces the unobfuscate logic to produce a readable image.

DISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only.

# Usage
```
usage: unobfuscate.py [-h] obfuscated_image unobfuscated_image

Unobfuscate manage page image.

positional arguments:
  obfuscated_image    Path to the obfuscated image.
  unobfuscated_image  Output path to the obfuscated image.

options:
  -h, --help          show this help message and exit
```

# Example
```
>>> python unobfuscate.py raw1.jpg page1.jpg

Successfully unobfuscated image at: page1.jpg
```

# Docker
```
>>> docker build -t viz .
>>> docker run -v /home/user/images/:/app/images viz images/raw1.jpg images/page1.jpg

Successfully unobfuscated image at: images/page1.jpg
```