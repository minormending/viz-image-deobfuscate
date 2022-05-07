# Viz Manga Unobfuscator

Viz manga pages are delivered to the browser as obfuscated images and the client JS is responsible for unobfuscating those images for the viewer to read. This program reproduces the unobfuscate logic to produce a readable image.

`obfuscated image:`
![obfuscated image](https://github.com/minormending/viz-image-unobfuscate/tree/main/images/raw1.png)

`unobfuscated image:`
![obfuscated image](https://github.com/minormending/viz-image-unobfuscate/tree/main/images/page1.png)

The image Exif metadata stores a hex digest to unobfuscate the image. Using the each byte value of the digest with it's position in the digest, we can select the appropriate tile in the obfuscated image and put it in the proper place in the unobfuscated image.  

DISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only.

# Installation 
```
pip install viz-image-unobfuscate 
```


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