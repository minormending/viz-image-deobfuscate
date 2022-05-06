from typing import Any, Dict, List
from math import floor
from PIL import Image
import piexif
import logging

logging.basicConfig(level=logging.DEBUG)

class VizImage:
    def _get_exif_key(self, image_loc: str) -> List[int]:
        metadata: Dict[str, Any] = piexif.load(image_loc)
        ifd: Dict[int, Any] = metadata.get("Exif")
        if ifd:
            tag: int = 42016 # 0xA420 # ImageUniqueID
            key: bytes = ifd.get(tag)
            if key:
                hex: List[str] = key.decode().split(":")
                return [int(h, 16) for h in hex]
            else:
                logging.warning(f"Unable to find Exif ImageUniqueID ({tag}) ifd tag for image: {image_loc}")
        else:
            logging.warning(f"Unable to find Exif metadata for image: {image_loc}")
        return []

    def _draw_image(self, dest_image: Image, src_image: Image, src_x: int, src_y: int, src_width: int, src_height: int, dest_x: int, dest_y: int) -> None:
        cropped_image: Image = src_image.crop(box=(src_x, src_y, src_x + src_width, src_y + src_height))
        dest_image.paste(cropped_image, (dest_x, dest_y))

    def unobfuscate_image(self, image_name: str, width: int, height: int) -> Image:
        keys: List[int] = self._get_exif_key(image_name)

        obfuscated_image: Image = Image.open(image_name)
        unobfuscated_image: Image = Image.new("RGB", size=(width, height), color="white")
        tile_width = floor(width / 10)
        tile_height = floor(height / 15)

        self._draw_image(unobfuscated_image, obfuscated_image, 0, 0, width, tile_height, 0, 0)
        self._draw_image(unobfuscated_image, obfuscated_image, 0, tile_height + 10, tile_width, height - 2 * tile_height, 0, tile_height)
        self._draw_image(unobfuscated_image, obfuscated_image, 0, 14 * (tile_height + 10), width, obfuscated_image.height - 14 * (tile_height + 10), 0, 14 * tile_height)
        self._draw_image(unobfuscated_image, obfuscated_image, 9 * (tile_width + 10), tile_height + 10, tile_width + (width - 10 * tile_width), height - 2 * tile_height, 9 * tile_width, tile_height)

        for idx, key in enumerate(keys):
            self._draw_image(
                unobfuscated_image,
                obfuscated_image, 
                floor((idx % 8 + 1) * (tile_width + 10)), 
                floor((floor(idx / 8) + 1) * (tile_height + 10)), 
                floor(tile_width), floor(tile_height), 
                floor((key % 8 + 1) * tile_width), 
                floor((floor(key / 8) + 1) * tile_height)
            )
        return unobfuscated_image


if __name__ == "__main__":
    obfuscated_image_name: str = "1.jpg"
    width: int = 784
    height: int = 1145 
    client = VizImage()
    unobfuscated_image: Image = client.unobfuscate_image(obfuscated_image_name, width, height)
    unobfuscated_image.save("page.jpg")