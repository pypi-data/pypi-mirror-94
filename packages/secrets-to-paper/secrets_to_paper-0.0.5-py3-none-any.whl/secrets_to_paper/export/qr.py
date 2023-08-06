import subprocess
import base64
import os
import io
import errno
import jinja2
import qrcode
from PIL import Image
from itertools import zip_longest
from weasyprint import HTML, CSS


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def get_qr_codes(data):
    """
    Expects binary data to be chunked into a list of base64 image strings
    """

    MAX_QR_BITS = 450
    chunks = (len(data) // MAX_QR_BITS) + 1

    qr_codes = []
    for chunk in split(data, chunks):
        chunk = [x for x in chunk if x]

        # Set version to None and use the fit parameter when making the code to
        # determine this automatically.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=2,
            border=4,
        )

        qr.add_data(bytes(chunk))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

    return qr_codes
