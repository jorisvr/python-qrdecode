#!/usr/bin/env python3

"""Decode a QR code from an image file."""

import sys
import argparse
from PIL import Image
import qrdecode


def main():

    parser = argparse.ArgumentParser(
        description="Decode a QR code from an image file.")
    parser.add_argument("--debug",
                        type=int,
                        help="debug level (0..3)")
    parser.add_argument("--repr",
                        action="store_true",
                        help="show result in Python repr format")
    parser.add_argument("image_file",
                        type=str,
                        help="file name of image containing the QR code")
    args = parser.parse_args()

    try:
        img = Image.open(args.image_file, "r")
    except IOError as exc:
        print("ERROR: Can not read image file -", exc, file=sys.stderr)
        return 1

    try:
        if args.debug is not None:
            data_bytes = qrdecode.decode_qrcode(img, debug_level=args.debug)
        else:
            data_bytes = qrdecode.decode_qrcode(img)
    except qrdecode.QRDecodeError as exc:
        print("ERROR: Can not decode QR code -", exc, file=sys.stderr)
        return 1

    data_str = data_bytes.decode("iso8859-1")
    if args.repr:
        print(repr(data_str))
    else:
        print(data_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())

