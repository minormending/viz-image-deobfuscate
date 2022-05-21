from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
from math import floor
from PIL import Image
import piexif
import logging


@dataclass
class Point:
    x: int
    y: int

    def loc(self) -> Tuple[int, int]:
        return (self.x, self.y)


@dataclass
class Size:
    width: int
    height: int


@dataclass
class Box:
    point: Point
    size: Size

    def region(self) -> Tuple[int, int, int, int]:
        return (
            self.point.x,
            self.point.y,
            self.point.x + self.size.width,
            self.point.y + self.size.height,
        )


def _get_exif_key(image_loc: str) -> List[int]:
    metadata: Dict[str, Any] = piexif.load(image_loc)
    ifd: Dict[int, Any] = metadata.get("Exif")
    if ifd:
        tag: int = 42016  # 0xA420 # ImageUniqueID
        key: bytes = ifd.get(tag)
        if key:
            hex: List[str] = key.decode().split(":")
            return [int(h, 16) for h in hex]
        else:
            logging.warning(
                f"Unable to find Exif ImageUniqueID ({tag}) ifd tag for image: {image_loc}"
            )
    else:
        logging.warning(f"Unable to find Exif metadata for image: {image_loc}")
    return []


def _draw_image(
    dest_image: Image, src_image: Image, src_box: Box, dest_point: Point
) -> None:
    cropped_image: Image = src_image.crop(box=src_box.region())
    dest_image.paste(cropped_image, dest_point.loc())


def deobfuscate_image(image_name: str) -> Image:
    keys: List[int] = _get_exif_key(image_name)
    if not keys:
        return None

    obfuscated_image: Image = Image.open(image_name)

    spacing: int = 10
    columns: int = 10
    rows: int = 15
    width: int = obfuscated_image.width - (columns - 1) * spacing
    height: int = obfuscated_image.height - (rows - 1) * spacing

    deobfuscated_image: Image = Image.new("RGB", size=(width, height), color="white")

    tile_width: int = floor(width / 10)
    tile_height: int = floor(height / 15)

    # The bounding 'tiles' are the actual edges of the page, so copy the over.
    _draw_image(  # top
        deobfuscated_image,
        obfuscated_image,
        Box(Point(0, 0), Size(width, tile_height)),
        Point(0, 0),
    )
    _draw_image(  # left
        deobfuscated_image,
        obfuscated_image,
        Box(
            Point(0, tile_height + spacing), Size(tile_width, height - 2 * tile_height)
        ),
        Point(0, tile_height),
    )
    _draw_image(  # bottom
        deobfuscated_image,
        obfuscated_image,
        Box(
            Point(0, (rows - 1) * (tile_height + spacing)),
            Size(width, obfuscated_image.height - (rows - 1) * (tile_height + spacing)),
        ),
        Point(0, (rows - 1) * tile_height),
    )
    _draw_image(  # right
        deobfuscated_image,
        obfuscated_image,
        Box(
            Point((columns - 1) * (tile_width + spacing), tile_height + spacing),
            Size(tile_width + (width - columns * tile_width), height - 2 * tile_height),
        ),
        Point((columns - 1) * tile_width, tile_height),
    )

    for idx, key in enumerate(keys):
        # move each center tile to their proper location
        _draw_image(
            deobfuscated_image,
            obfuscated_image,
            Box(
                Point(
                    floor((idx % 8 + 1) * (tile_width + spacing)),
                    floor((floor(idx / 8) + 1) * (tile_height + spacing)),
                ),
                Size(floor(tile_width), floor(tile_height)),
            ),
            Point(
                floor((key % 8 + 1) * tile_width),
                floor((floor(key / 8) + 1) * tile_height),
            ),
        )
    return deobfuscated_image

