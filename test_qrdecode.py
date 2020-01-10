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

    def test_all_versions_slow(self):
        fill_factor = {"L": 0.8, "M": 0.6, "Q": 0.44, "H": 0.33}
        for ver in range(1, 41):
            for errlvl in "LMQH":
                with self.subTest(ver=ver, errlvl=errlvl):
                    nchar = int((2 * ver**2 + 12 * ver) * fill_factor[errlvl])
                    text = self.gen_text_8bit(nchar)
                    self.run_test(text, ver=ver, errlvl=errlvl)


# TODO : test different scale factors
# TODO : test awkward rescale factors
# TODO : test rotated QR codes
# TODO : test damaged QR codes


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

