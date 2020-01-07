#!/usr/bin/env python3

"""Tests for QR decoder."""

import os.path
import unittest
from PIL import Image
import qrdecode


class TestImageFiles(unittest.TestCase):
    """Test QR decoding based on a collection of image files."""

    testdata_dir = os.path.join(os.path.dirname(__file__), "testdata")

    def run_test(self, image_file, expect_text):
        image_path = os.path.join(self.testdata_dir, image_file)
        img = Image.open(image_path, "r")
        got_bytes = qrdecode.decode_qrcode(img)
        got_text = got_bytes.decode("iso8859-1")
        self.assertEqual(got_text, expect_text)

    def test_qr_1(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test("Qr-1.png", "Ver1")

    def test_qr_2(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test("Qr-2.png", "Version 2")

    def test_qr_2(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test("Qr-2.png", "Version 2")

    def test_qr_3(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test("Qr-3.png", "Version 3 QR Code")

    def test_qr_4(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test("Qr-4.png", "Version 4 QR Code, up to 50 char")

    def test_qr_code_ver_10(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test(
            "Qr-code-ver-10.png",
            "VERSION 10 QR CODE, UP TO 174 CHAR AT H LEVEL, WITH 57X57 MODULES AND PLENTY OF ERROR CORRECTION TO GO AROUND.  NOTE THAT THERE ARE ADDITIONAL TRACKING BOXES")

    def test_qr_code_damaged(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test(
            "212px-QR_Code_Damaged.jpg",
            "http://en.m.wikipedia.org")

    def test_qrcode_1_intro(self):
        # source: https://en.wikipedia.org/wiki/Qr_code
        self.run_test(
            "QRCode-1-Intro.png",
            "Mr. Watson, come here - I want to see you.")

    def test_quart_6l(self):
        # generated with: https://research.swtch.com/qr/draw
        self.run_test(
            "qart_6L.png",
            "https://en.wikipedia.org/wiki/QR_code#341341429383959992563502682682330681341338447619959960012341266701351499272032042722683958594681341576255958516914682685346677341342913097959958005362682679603298597341320063959955263438682681344687341343681007959976000853426")


class TestWithGeneratedQrCodes(unittest.TestCase):
    """Test decoding of programatically generated QR codes.

    This requires the Python module "qrcode".
    See also http://github.com/lincolnloop/python-qrcode
    """

    def gen_qr_code(self, data, ver=None, errlvl=None, mask=None, box_size=3):
        """Generate a QR code with specified data and properties.

        Return the QR code as a PIL image.
        """

        # Lazy import of "qrcode". This way the image file tests can
        # run even when the module "qrcode" is not installed.
        import qrcode
        import qrcode.image.pil

        kwargs = {}
        kwargs["box_size"] = box_size
        if ver is not None:
            kwargs["version"] = ver
        if errlvl is not None:
            kwargs["error_correction"] = {
                "L": qrcode.ERROR_CORRECT_L,
                "M": qrcode.ERROR_CORRECT_M,
                "Q": qrcode.ERROR_CORRECT_Q,
                "H": qrcode.ERROR_CORRECT_H
            }[errlvl]
        if mask is not None:
            kwargs["mask_pattern"] = mask
        qr = qrcode.QRCode(**kwargs)
        qr.add_data(data)
        qr.make(fit=False)
        return qr.make_image(image_factory=qrcode.image.pil.PilImage)

    def gen_text_8bit(self, nchar, start):
        """Generate a test string containing 8-bit bytes."""
        data = bytearray(nchar)
        v = start
        for i in range(nchar):
            data[i] = v
            v = (v + 17) % 127
        return data.decode("ascii")

    def run_test(self, data, **kwargs):
        """Generate a QR code, then decode it and verify the decoding."""
        img = self.gen_qr_code(data, **kwargs)
        got_bytes = qrdecode.decode_qrcode(img)
        got_text = got_bytes.decode("iso8859-1")
        self.assertEqual(got_text, data)

    #
    # Test an empty code (0 characters).
    #

    def test_1l_empty(self):
        self.run_test("", ver=1, errlvl="L")

    #
    # Test version-1 codes with all different error correction levels.
    #

    def test_1l(self):
        self.run_test("abcdefghijklmnop", ver=1, errlvl="L")

    def test_1m(self):
        self.run_test("qrstuvwxyz0123", ver=1, errlvl="M")

    def test_1q(self):
        self.run_test("4567abcdef", ver=1, errlvl="Q")

    def test_1h(self):
        self.run_test("ghijklm", ver=1, errlvl="H")

    #
    # Test progressively larger QR codes.
    #

    def test_6l(self):
        text = self.gen_text_8bit(125, 0)
        self.run_test(text, ver=6, errlvl="L")

    def test_8m(self):
        text = self.gen_text_8bit(145, 17)
        self.run_test(text, ver=8, errlvl="M")

    def test_12q(self):
        text = self.gen_text_8bit(195, 25)
        self.run_test(text, ver=12, errlvl="Q")

    def test_20h(self):
        text = self.gen_text_8bit(375, 42)
        self.run_test(text, ver=20, errlvl="H")

    def test_40h(self):
        text = self.gen_text_8bit(1265, 51)
        self.run_test(text, ver=40, errlvl="H")

    # TODO : test all mask patterns
    # TODO : test all encodings
    # TODO : test all (version, error_correction) combinations


if __name__ == "__main__":
    unittest.main()

