from PIL import Image
from viz_image_deobfuscate import deobfuscate_image


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Deobfuscate manage page image.")
    parser.add_argument("obfuscated_image", help="Path to the obfuscated image.")
    parser.add_argument(
        "deobfuscated_image", help="Output path to the obfuscated image."
    )

    args = parser.parse_args()

    deobfuscated_image: Image = deobfuscate_image(args.obfuscated_image)
    if deobfuscate_image:
        deobfuscated_image.save(args.deobfuscated_image)
        print(f"Successfully deobfuscated image at: {args.deobfuscated_image}")
    else:
        print(f"Unable to deobfuscate image, check image Exif data.")
        exit(1)


if __name__ == "__main__":
    main()