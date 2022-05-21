# Viz Manga Deobfuscator

Viz manga pages are delivered to the browser as obfuscated images and the client JS is responsible for deobfuscation of those images for the viewer to read. This program reproduces the deobfuscate logic to produce a readable image.

`obfuscated image:`
![obfuscated image](https://raw.githubusercontent.com/minormending/viz-image-deobfuscate/main/images/raw1.jpg)

`deobfuscated image:`
![deobfuscated image](https://raw.githubusercontent.com/minormending/viz-image-deobfuscate/main/images/page1.jpg)

The image Exif metadata stores a hex digest to deobfuscate the image. Using the each byte value of the digest with it's position in the digest, we can select the appropriate tile in the obfuscated image and put it in the proper place in the deobfuscated image.  

DISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only.

# Installation 
```
pip install viz-image-deobfuscate 
```

# Usage
This package exposes `deobfuscate_image` that accepts a path to an image and returns an PIL `Image` of the deobfuscated image.

```
from viz_image_deobfuscate import deobfuscate_image

deobfuscated = deobfuscate_image("raw.jpg")
deobfuscated.save("page.jpg")
```

# CLI Usage
Bundled with this package is a CLI tool for scripting/testing purposes.

```
usage: image-deobfuscate-cli [-h] obfuscated_image deobfuscated_image

Deobfuscate manage page image.

positional arguments:
  obfuscated_image    Path to the obfuscated image.
  deobfuscated_image  Output path to the obfuscated image.

options:
  -h, --help          show this help message and exit
```

## Example
```
>>> image-deobfuscate-cli raw1.jpg page1.jpg

Successfully deobfuscated image at: page1.jpg
```

# Docker
Alternatively, you can build your own docker container to run the CLI or download an already built container from [Docker Hub](https://hub.docker.com/r/minormending/viz-image-deobfuscate)

```
>>> docker build -t viz .
>>> docker run -v /home/user/images/:/app/images viz images/raw1.jpg images/page1.jpg

Successfully deobfuscated image at: images/page1.jpg
```