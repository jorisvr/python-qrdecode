python-qrdecode
===============

`qrdecode.py` is a Python 3 module for decoding QR codes from image data.

This module can only process computer-generated images containing a clean, undamaged QR code.
It can not be used to process QR codes from photographs or scanned images.


Features
--------

Supported:
- Automatic detection of the QR code location within the image.
- Automatic detection of QR code size and scale factor.
- Reed-Solomon error correction of damaged QR codes.
- Model 2 QR codes, version 1 to 40 (all sizes).

Not supported:
- Rotation of the QR code over arbitrary angles (only 90, 180, 270 degrees).
- Non-uniform scaling of the QR code.
- Images with bad contrast or noise.
- Error correction of version information or format information fields in the QR code.
- ECI (Extended Channel Interpretation), for example non-default character sets.
- Model 1 QR codes or other types of 2D bar codes.


Status
------

This is a toy project.
Do not use this module in production-level software.

The image processing algorithms in this module are unsophisticated.
Decoding of screen-captured QR codes seems to work reliably.
Decoding of photographed QR codes has not been tested and will probably not work.

The algorithms are implemented in Python (with Numpy), which makes this code relatively slow.


Dependencies
------------

- Python 3 (tested with Python 3.7.3)
- Numpy (tested with Numpy 1.16.2)
- Pillow, the Python Imaging Library (tested with Pillow 5.4.1)
- to test the QR decoder (optional): https://github.com/lincolnloop/python-qrcode


API
---

```python
  import qrdecode
  from PIL import Image

  # Read image file.
  img = Image.open("image_file.png", "r")

  # Decode QR code.
  data = qrdecode.decode_qrcode(img)

  # Show results.
  print("Text in QR code:", data)

  # If you want lots of debug information about the QR decoding process:
  data = qrdecode.decode_qrcode(img, debug_level=3)
```


Command-line program
--------------------

`decode_qrcode.py` is a command-line Python program which reads an image file and decodes a QR code from the image.
The data from the decoded QR code is printed to stdout.

```
Usage:
  python3 decode_qrcode.py [--debug=level] [--repr] "image_file.png"

  --debug=level   sets the level of debug messages (0..3, default=0)
  --repr          shows the QR code data in Python repr() format
```


Tests
-----

The Python program `test_qrdecode.py` runs the QR decoder on a test suite
consisting of images with many different QR codes.

Some of the test cases are image files from the `testdata` directory.
Other test cases use a QR code generator (https://github.com/lincolnloop/python-qrcode) to create test images on the fly.

