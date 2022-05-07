from typing import Any, Dict, List
from math import floor
from PIL import Image
import piexif
import logging


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
    dest_image: Image,
    src_image: Image,
    src_x: int,
    src_y: int,
    src_width: int,
    src_height: int,
    dest_x: int,
    dest_y: int,
) -> None:
    cropped_image: Image = src_image.crop(
        box=(src_x, src_y, src_x + src_width, src_y + src_height)
    )
    dest_image.paste(cropped_image, (dest_x, dest_y))


def unobfuscate_image(image_name: str) -> Image:
    keys: List[int] = _get_exif_key(image_name)
    if not keys:
        return None

    obfuscated_image: Image = Image.open(image_name)

    spacing: int = 10
    columns: int = 10
    rows: int = 15
    width: int = obfuscated_image.width - (columns - 1) * spacing
    height: int = obfuscated_image.height - (rows - 1) * spacing

    unobfuscated_image: Image = Image.new("RGB", size=(width, height), color="white")

    tile_width: int = floor(width / 10)
    tile_height: int = floor(height / 15)

    # The bounding 'tiles' are the actual edges of the page, so copy the over.
    _draw_image(  # top
        unobfuscated_image, obfuscated_image, 0, 0, width, tile_height, 0, 0
    )
    _draw_image(  # left
        unobfuscated_image,
        obfuscated_image,
        0,
        tile_height + spacing,
        tile_width,
        height - 2 * tile_height,
        0,
        tile_height,
    )
    _draw_image(  # bottom
        unobfuscated_image,
        obfuscated_image,
        0,
        (rows - 1) * (tile_height + spacing),
        width,
        obfuscated_image.height - (rows - 1) * (tile_height + spacing),
        0,
        (rows - 1) * tile_height,
    )
    _draw_image(  # right
        unobfuscated_image,
        obfuscated_image,
        (columns - 1) * (tile_width + spacing),
        tile_height + spacing,
        tile_width + (width - columns * tile_width),
        height - 2 * tile_height,
        (columns - 1) * tile_width,
        tile_height,
    )

    for idx, key in enumerate(keys):
        # move each center tile to their proper location
        _draw_image(
            unobfuscated_image,
            obfuscated_image,
            floor((idx % 8 + 1) * (tile_width + spacing)),
            floor((floor(idx / 8) + 1) * (tile_height + spacing)),
            floor(tile_width),
            floor(tile_height),
            floor((key % 8 + 1) * tile_width),
            floor((floor(key / 8) + 1) * tile_height),
        )
    return unobfuscated_image


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Unobfuscate manage page image.")
    parser.add_argument("obfuscated_image", help="Path to the obfuscated image.")
    parser.add_argument(
        "unobfuscated_image", help="Output path to the obfuscated image."
    )

    args = parser.parse_args()

    unobfuscated_image: Image = unobfuscate_image(args.obfuscated_image)
    if unobfuscate_image:
        unobfuscated_image.save(args.unobfuscated_image)
        print(f"Successfully unobfuscated image at: {args.unobfuscated_image}")
    else:
        print(f"Unable to unobfuscate image, check image Exif data.")
        exit(1)
