#!/usr/bin/env python3

"""Tests program for QR decoder."""

import sys
import os.path
import json
from PIL import Image
import qrdecode


def run_test(data_dir, image_file, expect_text):

    print("Testing", image_file, "...", end=" ")
    sys.stdout.flush()

    image_path = os.path.join(data_dir, image_file)
    img = Image.open(image_path, "r")

    got_text = None
    got_exception = None
    try:
        got_bytes = qrdecode.decode_qrcode(img)
        got_text = got_bytes.decode("iso8859-1")
        ok = (got_text == expect_text)
    except qrdecode.QRDecodeError as exc:
        ok = False
        got_exception = exc

    if ok:
        print("ok")
    else:
        print("FAILED")
        if got_text is not None:
            print("  got", repr(got_text))
        elif got_exception is not None:
            print("  got QRDecodeError:", got_exception)
        print("  expected", repr(expect_text))

    return ok


def read_file_info(data_dir):
    file_info_path = os.path.join(data_dir, "file_info.json")
    with open(file_info_path, "r") as f:
        file_info = json.load(f)
    return file_info


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "testdata")
    file_info = read_file_info(data_dir)

    ntest = 0
    nfail = 0
    for test_image in file_info:
        image_file = test_image["file"]
        expect_text = test_image["text"]
        ok = run_test(data_dir, image_file, expect_text)
        ntest += 1
        if not ok:
            nfail += 1

    print("DONE - {} failures in {} tests".format(nfail, ntest))

    if nfail != 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

