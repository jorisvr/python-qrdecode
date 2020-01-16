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

    def test_qr_code_embedded(self):
        # version-30 QR code which contains a valid version-2 QR code
        raw_data = bytes([
105,33,97,132,193,97,108,193,99,189,204,49,97,79,4,230,108,130,53,224,
198,25,99,60,198,97,129,97,97,5,84,145,108,61,81,156,200,97,97,150,
52,252,201,34,108,193,140,33,101,101,60,195,1,108,193,106,165,83,97,96,
138,81,110,29,96,119,189,85,82,97,105,72,120,65,101,121,202,169,33,97,
82,220,58,163,105,64,4,145,97,106,192,1,97,106,162,97,97,96,246,33,
97,97,101,82,65,97,97,97,97,97,97,97,97,97,97,100,145,102,22,65,
107,76,193,145,56,208,193,105,35,252,70,97,103,40,83,1,97,35,108,198,
100,1,49,108,55,82,65,96,197,217,236,193,129,98,67,52,156,193,102,76,
198,17,97,70,62,140,200,34,108,201,110,165,99,97,99,10,81,110,17,104,
116,127,213,81,97,111,152,113,96,223,93,154,164,225,111,210,208,201,103,63,
144,2,81,97,99,0,97,97,106,161,81,97,96,241,97,161,97,101,89,97,
97,97,97,97,97,97,97,97,97,104,50,65,104,108,97,99,140,201,155,28,
131,1,100,144,62,198,97,147,126,140,49,100,145,108,198,97,98,225,96,193,
105,33,99,21,76,60,198,17,105,35,48,60,195,62,76,200,97,105,35,61,
156,193,100,204,201,97,97,195,49,104,58,84,174,17,104,123,69,229,74,166,
116,248,113,98,215,252,218,161,97,101,242,209,97,134,116,240,5,81,97,108,
49,225,97,106,165,81,97,96,241,101,161,97,101,81,65,97,97,97,97,97,
97,97,97,97,96,137,33,97,132,49,101,108,201,147,189,204,97,98,79,4,
225,105,146,53,224,193,98,65,108,198,97,150,97,99,1,100,145,105,145,50,
172,152,97,100,147,62,81,99,55,188,193,129,100,147,53,60,194,44,204,201,
97,99,195,49,96,170,89,206,17,120,119,177,97,106,163,105,72,113,98,213,
121,234,160,7,189,82,209,103,131,105,64,5,81,97,96,193,225,97,97,101,
81,97,96,241,101,161,97,101,96,1,97,97,97,97,97,97,97,97,97,99,
1,97,102,19,49,96,124,201,145,56,209,100,25,35,252,65,89,151,40,83,
97,105,33,108,193,105,155,1,108,49,99,65,105,147,50,57,241,72,50,67,
57,162,163,56,60,150,97,98,67,49,81,98,38,204,201,97,99,195,49,1,
106,89,206,16,104,116,113,101,90,167,63,153,97,114,223,81,97,96,4,127,
210,209,103,135,63,224,5,81,97,99,97,225,97,97,133,81,97,97,97,101,
161,97,97,96,1,97,97,97,97,97,97,97,97,97,104,33,97,104,67,49,
100,33,9,155,28,134,104,68,144,62,197,121,147,126,129,101,84,145,108,192,
57,151,161,64,228,156,164,201,147,48,58,28,192,137,35,49,106,227,53,201,
113,74,185,35,57,160,98,36,204,153,97,99,195,63,1,97,105,201,81,8,
107,97,101,218,166,116,241,5,114,215,241,100,48,11,69,243,97,103,134,113,
97,101,81,103,129,97,225,97,102,21,81,97,97,4,149,161,97,104,96,1,
97,97,97,97,97,97,97,97,97,97,97,97,97,108,195,49,101,100,25,99,
189,198,97,143,12,229,5,89,146,53,230,109,82,65,97,98,105,159,76,241,
104,201,142,185,147,61,254,204,195,1,108,194,26,163,52,227,60,202,164,163,
49,100,194,44,73,145,105,51,195,63,10,225,105,197,86,17,97,82,213,90,
163,105,64,5,82,229,97,96,192,7,189,81,89,39,131,97,99,5,65,103,
129,97,225,101,168,101,81,97,96,2,69,97,97,97,128,1,97,97,97,97,
97,97,97,97,97,97,99,49,97,108,195,49,96,120,65,33,56,214,100,3,
252,76,55,89,103,40,86,101,209,97,96,195,41,145,109,102,105,138,220,169,
131,51,63,60,200,34,108,200,110,161,102,101,76,203,161,108,193,134,66,44,
201,154,161,147,227,63,10,161,105,197,80,97,111,210,221,73,103,63,144,7,
81,97,151,131,0,4,127,213,84,151,231,97,108,61,33,103,132,145,97,101,
161,161,97,97,96,9,33,97,111,6,16,1,97,97,97,97,97,97,97,97,
97,97,99,49,97,108,195,1,100,97,132,155,28,134,97,96,62,192,193,97,
19,126,134,101,65,49,99,6,57,108,50,54,108,135,116,49,3,33,200,108,
193,102,140,193,129,97,38,52,92,202,162,108,198,28,97,108,105,154,163,17,
97,111,14,161,105,85,81,97,101,242,209,97,134,116,240,5,97,108,215,140,
33,107,69,245,82,65,96,240,112,205,33,103,130,65,97,101,161,99,1,97,
96,4,97,97,111,8,97,97,97,97,97,97,97,97,97,97,97,97,99,49,
97,108,201,33,99,5,98,67,189,198,97,159,4,227,1,98,66,53,230,97,
99,49,108,49,97,67,98,86,102,105,162,102,16,153,194,76,195,52,76,198,
17,100,147,52,28,193,101,92,200,97,97,150,57,154,169,35,97,111,10,161,
97,53,80,7,189,82,209,103,131,105,64,1,113,105,199,129,96,119,189,85,
89,97,105,72,115,13,33,103,137,33,97,101,161,111,1,97,96,1,97,97,
111,1,96,241,97,97,97,97,97,97,97,97,97,97,99,49,97,108,196,145,
124,49,105,33,56,209,105,147,252,76,49,105,39,40,86,97,147,49,96,193,
105,33,103,38,102,106,182,96,98,73,192,145,99,49,220,200,97,98,67,55,
60,195,57,92,193,129,102,19,57,154,161,99,97,96,10,161,97,53,80,4,
127,210,209,103,135,63,224,5,87,93,151,129,104,116,127,213,81,97,111,152,
113,109,33,102,164,225,97,101,161,111,1,97,96,42,161,97,111,1,96,241,
97,97,97,97,97,97,97,97,97,97,99,49,97,106,162,64,112,197,84,155,
28,128,57,144,62,192,225,100,147,126,129,105,147,49,99,1,100,145,106,182,
102,99,99,49,105,41,89,160,99,57,124,145,97,105,35,51,81,99,53,140,
198,17,108,51,57,154,165,83,97,96,10,161,97,49,0,11,69,243,97,119,
134,113,97,101,87,252,215,129,104,123,69,229,74,166,116,248,113,109,33,106,
160,1,97,101,97,95,1,97,97,106,161,97,111,1,96,241,97,97,97,97,
97,97,97,97,97,97,97,97,97,107,169,33,99,13,82,83,189,194,105,159,
4,225,100,146,66,53,224,25,147,49,76,97,98,65,98,161,102,97,96,49,
100,145,49,100,195,49,121,113,73,52,147,57,160,35,61,156,152,97,100,147,
57,145,101,83,97,96,10,161,97,108,144,7,189,81,82,103,131,97,96,69,
85,121,199,97,104,119,177,97,106,163,105,72,113,121,97,106,160,1,97,97,
162,79,1,97,102,26,161,97,109,97,64,241,97,97,97,97,97,97,97,97,
97,97,97,145,97,106,180,155,76,53,209,48,216,195,41,147,252,70,104,201,
39,40,80,105,147,60,193,100,25,33,108,193,86,97,96,193,98,76,193,134,
67,58,84,12,193,146,99,49,96,195,60,89,81,72,54,19,57,162,165,83,
97,96,10,161,97,104,192,4,127,213,83,39,231,97,97,133,95,93,145,36,
152,116,113,96,202,167,63,153,98,65,97,106,160,1,97,106,169,47,97,97,
104,106,161,97,97,89,32,241,97,97,97,97,97,97,97,97,97,97,98,65,
97,106,161,99,225,69,75,28,131,6,57,96,62,198,105,131,118,142,49,9,
147,60,198,104,68,129,97,101,113,33,99,5,89,108,198,28,97,106,97,92,
195,17,108,192,98,3,53,147,28,192,140,35,49,106,229,83,97,96,10,145,
97,121,129,107,69,245,86,49,96,240,116,21,87,252,218,162,72,107,97,99,
10,166,116,241,9,33,97,106,160,1,97,106,164,145,97,96,241,138,161,97,
101,84,144,97,97])
        self.run_test("qr_code_embedded.png", raw_data.decode("iso8859-1"))

    def test_qr_code_embedded_inner(self):
        # broken version-30 QR code which contains a valid version-2 QR code
        self.run_test("qr_code_embedded_inner.png", "Little code")

    def test_qr_damaged_1L(self):
        # single bit changed
        self.run_test("qr_damaged_1L.png", "just 1 bit error.")

    def test_qr_damaged_1Q(self):
        self.run_test("qr_damaged_1Q.png", "damaged qr.")

    def test_qr_damaged_7H(self):
        # Two of the error correction blocks contain the maximum number of
        # correctable errors.
        # Block 1 has all 13 data words modified.
        # Block 5 has 13 error correction words modified.
        self.run_test(
            "qr_damaged_7H.png",
            "Maximum number of correctable errors in two blocks of this code.")

    def test_qr_damaged_8L(self):
        # Light damage to QR code image.
        self.run_test(
            "qr_damaged_8L.png",
            "A version 8 code with low error correction. Funny thing that version 8L can store more data than version 12H. It shows the extreme amount of redundancy used in error correction level H.")

    def test_qr_damaged_9Q(self):
        # "Logo" decoration pasted over the middle of the QR code.
        self.run_test(
            "qr_damaged_9Q.png",
            "QR codes are sometimes intentionally damaged by putting a decoration on top of the code. This relies on the error correction.")

    def test_qr_damaged_12H(self):
        # Damaged by drawing on a big part of the QR code.
        self.run_test(
            "qr_damaged_12H.png",
            "A version 12 code with high error correction. We can mess it up pretty bad and still decode it correctly. Those Reed-Solomon codes are quite impressive.")


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

    def gen_text_numeric(self, nchar):
        """Generate a test string containing decimal digits."""
        data_chars = [str(i % 10) for i in range(nchar)]
        return "".join(data_chars)

    def gen_text_alphanum(self, nchar):
        """Generate a test string containing alphanumeric characters."""
        alphanum = [str(i) for i in range(10)]
        alphanum += [chr(ord("A") + i) for i in range(26)]
        alphanum += list(" $%*+-./:")
        assert len(alphanum) == 45
        data_chars = [alphanum[(2*i) % 45] for i in range(nchar)]
        return "".join(data_chars)

    def gen_text_8bit(self, nchar):
        """Generate a test string containing 8-bit bytes."""
        data_chars = [chr((5 * i + 97) % 127) for i in range(nchar)]
        return "".join(data_chars)

    def check_qr_code(self, img, expect_text):
        """Decode a QR code and verify that it is decoded correctly."""
        got_bytes = qrdecode.decode_qrcode(img)
        got_text = got_bytes.decode("iso8859-1")
        self.assertEqual(got_text, expect_text)

    def run_test(self, data, **kwargs):
        """Generate a QR code, then decode it and verify the decoding."""
        img = self.gen_qr_code(data, **kwargs)
        self.check_qr_code(img, data)

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
    # Test larger QR codes.
    #

    def test_6l(self):
        text = self.gen_text_8bit(125)
        self.run_test(text, ver=6, errlvl="L")

    def test_8m(self):
        text = self.gen_text_8bit(145)
        self.run_test(text, ver=8, errlvl="M")

    def test_12q(self):
        text = self.gen_text_8bit(195)
        self.run_test(text, ver=12, errlvl="Q")

    def test_20h(self):
        text = self.gen_text_8bit(375)
        self.run_test(text, ver=20, errlvl="H")

    def test_40h(self):
        text = self.gen_text_8bit(1265)
        self.run_test(text, ver=40, errlvl="H")

    #
    # Test different character encoding modes.
    #

    def test_6m_numeric(self):
        text = self.gen_text_numeric(250)
        self.run_test(text, ver=6, errlvl="M")

    def test_7m_alphanumeric(self):
        text = self.gen_text_alphanum(170)
        self.run_test(text, ver=7, errlvl="M")

    def test_8m_mixed_mode(self):
        text = (self.gen_text_8bit(25)
                + self.gen_text_numeric(60)
                + self.gen_text_alphanum(35)
                + self.gen_text_8bit(24)
                + self.gen_text_numeric(55)
                + self.gen_text_alphanum(32))
        self.run_test(text, ver=8, errlvl="M")

    #
    # Test all mask patterns.
    #

    def test_mask_patterns(self):
        text = self.gen_text_8bit(145)
        for mask_pattern in range(8):
            with self.subTest(mask_pattern=mask_pattern):
                self.run_test(text, ver=10, errlvl="Q", mask=mask_pattern)

    #
    # Test all combinations of QR version and error correction level.
    #

    def test_slow_all_versions(self):
        fill_factor = {"L": 0.8, "M": 0.6, "Q": 0.44, "H": 0.33}
        for ver in range(1, 41):
            for errlvl in "LMQH":
                with self.subTest(ver=ver, errlvl=errlvl):
                    nchar = int((2 * ver**2 + 12 * ver) * fill_factor[errlvl])
                    text = self.gen_text_8bit(nchar)
                    self.run_test(text, ver=ver, errlvl=errlvl)

    #
    # Test different scale factors.
    #

    def test_1m_scale10(self):
        text = self.gen_text_8bit(14)
        self.run_test(text, ver=1, errlvl="M", box_size=10)

    def test_1m_scale2(self):
        text = self.gen_text_8bit(14)
        self.run_test(text, ver=1, errlvl="M", box_size=2)

    def test_1m_scale1(self):
        text = self.gen_text_8bit(14)
        self.run_test(text, ver=1, errlvl="M", box_size=1)

    def test_40m_scale2(self):
        text = self.gen_text_8bit(2300)
        self.run_test(text, ver=40, errlvl="M", box_size=2)

    def test_40m_scale1(self):
        text = self.gen_text_8bit(2300)
        self.run_test(text, ver=40, errlvl="M", box_size=1)

    def test_1m_scale1p7(self):
        # Non-integer scale factor: 1.7 pixels per module.
        text = self.gen_text_8bit(14)
        img = self.gen_qr_code(text, ver=1, errlvl="M", box_size=1)

        (width, height) = img.size
        width = int(1.7 * width)
        height = int(1.7 * height)
        img = img.resize((width, height), resample=Image.NEAREST)

        self.check_qr_code(img, text)

    def test_40m_scale1p7(self):
        # Non-integer scale factor: 1.7 pixels per module.
        text = self.gen_text_8bit(2300)
        img = self.gen_qr_code(text, ver=40, errlvl="M", box_size=1)

        (width, height) = img.size
        width = int(1.7 * width)
        height = int(1.7 * height)
        img = img.resize((width, height), resample=Image.NEAREST)

        self.check_qr_code(img, text)

    def test_1m_scalexy(self):
        # Different X/Y scale factor: 2.3 x 1.9 pixels per module.
        text = self.gen_text_8bit(14)
        img = self.gen_qr_code(text, ver=1, errlvl="M", box_size=1)

        (width, height) = img.size
        width = int(2.3 * width)
        height = int(1.9 * height)
        img = img.resize((width, height), resample=Image.NEAREST)

        self.check_qr_code(img, text)

    def test_40m_scalexy(self):
        # Different X/Y scale factor: 2.3 x 1.9 pixels per module.
        text = self.gen_text_8bit(2300)
        img = self.gen_qr_code(text, ver=40, errlvl="M", box_size=1)

        (width, height) = img.size
        width = int(2.3 * width)
        height = int(1.9 * height)
        img = img.resize((width, height), resample=Image.NEAREST)

        self.check_qr_code(img, text)

    #
    # Test rotated QR codes (only 90, 180, 270 degrees).
    #

    def test_5q_rot90(self):
        # Note: version-5 QR codes do not contain version information.
        text = self.gen_text_8bit(55)
        img = self.gen_qr_code(text, ver=5, errlvl="Q")
        img = img.rotate(90)
        self.check_qr_code(img, text)

    def test_5q_rot180(self):
        text = self.gen_text_8bit(55)
        img = self.gen_qr_code(text, ver=5, errlvl="Q")
        img = img.rotate(180)
        self.check_qr_code(img, text)

    def test_5q_rot270(self):
        text = self.gen_text_8bit(55)
        img = self.gen_qr_code(text, ver=5, errlvl="Q")
        img = img.rotate(270)
        self.check_qr_code(img, text)

    def test_8q_rot90(self):
        # Note: version-8 QR codes contain version information.
        text = self.gen_text_8bit(95)
        img = self.gen_qr_code(text, ver=8, errlvl="Q")
        img = img.rotate(90)
        self.check_qr_code(img, text)

    def test_8q_rot180(self):
        text = self.gen_text_8bit(95)
        img = self.gen_qr_code(text, ver=8, errlvl="Q")
        img = img.rotate(180)
        self.check_qr_code(img, text)

    def test_8q_rot270(self):
        text = self.gen_text_8bit(95)
        img = self.gen_qr_code(text, ver=8, errlvl="Q")
        img = img.rotate(270)
        self.check_qr_code(img, text)

    #
    # Test rotated QR codes with different X/Y scaling.
    #

    def test_9h_rot90_scalexy(self):
        text = self.gen_text_8bit(90)
        img = self.gen_qr_code(text, ver=9, errlvl="H", box_size=1)

        img = img.rotate(90)
        (width, height) = img.size
        img = img.resize((3 * width, 4 * height))

        self.check_qr_code(img, text)

    def test_9h_rot180_scalexy(self):
        text = self.gen_text_8bit(90)
        img = self.gen_qr_code(text, ver=9, errlvl="H", box_size=1)

        img = img.rotate(180)
        img = img.rotate(90)
        (width, height) = img.size
        img = img.resize((3 * width, 4 * height))

        self.check_qr_code(img, text)

    def test_9h_rot270_scalexy(self):
        text = self.gen_text_8bit(90)
        img = self.gen_qr_code(text, ver=9, errlvl="H", box_size=1)

        img = img.rotate(270)
        img = img.rotate(90)
        (width, height) = img.size
        img = img.resize((3 * width, 4 * height))

        self.check_qr_code(img, text)


def dump_generated_qr_codes():
    """Dump the QR codes from TestWithGeneratedQrCodes as image files.

    This function is not normally used as part of the test, but it may
    be useful for debugging.
    """

    import contextlib
    import inspect

    var_test_name = [None]
    var_subtest = [None, None]

    # Prepare a patched version of the method "check_qr_code()"
    # which dumps the image to a file instead of decoding the QR code.
    def new_check_qr_code(img, expect_text):
        test_name = var_test_name[0]
        subtest_msg = var_subtest[0]
        subtest_args = var_subtest[1]
        fname = "gen_" + test_name
        if subtest_msg is not None:
            fname = fname + "_" + str(subtest_msg)
        if subtest_args is not None:
            for (k, v) in subtest_args.items():
                fname = fname + "_" + str(k) + str(v)
        fname = fname + ".png"
        fname = fname.replace("/", "_")
        fname = fname.replace("\\", "_")
        print("Writing", fname)
        img.save(fname)

    # Prepare a patched version of the method "subTest()" which captures
    # the subtest information.
    @contextlib.contextmanager
    def new_subTest(msg=None, **kwargs):
        var_subtest[0] = msg
        var_subtest[1] = kwargs
        try:
            yield None
        finally:
            var_subtest[0] = None
            var_subtest[1] = None

    # Create an instance of TestWithGneratedQrCodes and patch
    # the methods "check_qr_code()" and "subTest()".
    testcase = TestWithGeneratedQrCodes()
    testcase.check_qr_code = new_check_qr_code
    testcase.subTest = new_subTest

    # Call all test_XXX methods.
    methods = inspect.getmembers(testcase, inspect.ismethod)
    for (method_name, method) in methods:
        if method_name.startswith("test_"):
            # Store the test name, to be used when dumping images.
            var_test_name[0] = method_name[5:]
            var_subtest[0] = None
            var_subtest[1] = None
            # Invoke the test method.
            method()


if __name__ == "__main__":
    unittest.main()

