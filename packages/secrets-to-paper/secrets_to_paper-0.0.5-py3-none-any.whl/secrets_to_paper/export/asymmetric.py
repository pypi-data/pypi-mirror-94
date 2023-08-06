from secrets_to_paper.export import (
    templateEnv,
    templateLoader,
    write_pdf_to_disk,
)
from secrets_to_paper.export.qr import get_qr_codes
import subprocess
import base64
import os
import io
import errno
import jinja2
import qrcode
from PIL import Image
from itertools import zip_longest
from cryptography.hazmat.primitives.serialization import (
    PublicFormat,
    Encoding,
    NoEncryption,
    KeySerializationEncryption,
    PrivateFormat,
)
import datetime


def export_ecc(private_key, output, key_label=""):

    pemdata = private_key.private_bytes(
        Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption(),
    )

    pub_key = private_key.public_key()
    public_point = pub_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)

    public_key = pub_key.public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    ).decode("ascii")
    qr_codes = get_qr_codes(pemdata)

    secret_number = private_key.private_numbers().private_value
    public_point = public_point.hex()

    filename = output + ".pdf"
    template = templateEnv.get_template("ecc_key.html")

    rendered = template.render(
        ascii_key=pemdata.decode("ascii"),
        public_key=public_key,
        qr_images=qr_codes,
        key_label=key_label,
        secret_number=hex(secret_number),
        public_point=hex(int(public_point, 16)),
        key_size=private_key.curve.key_size,
        key_type=private_key.curve.name,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    )

    write_pdf_to_disk(rendered, filename)


def export_rsa(private_key, output, key_label=""):

    pemdata = private_key.private_bytes(
        Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption(),
    )

    private_numbers = private_key.private_numbers()
    public_numbers = private_key.public_key().public_numbers()

    qr_codes = get_qr_codes(pemdata)

    filename = output + ".pdf"
    template = templateEnv.get_template("rsa_key.html")

    rendered = template.render(
        qr_images=qr_codes,
        ascii_key=pemdata.decode("ascii"),
        key_label=key_label,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        key_type="RSA",
        key_size=private_key.key_size,
        p=hex(private_numbers.p),
        q=hex(private_numbers.q),
        d=hex(private_numbers.d),
        dmp1=hex(private_numbers.dmp1),
        dmq1=hex(private_numbers.dmq1),
        e=hex(public_numbers.e),
        n=hex(public_numbers.n),
    )

    write_pdf_to_disk(rendered, filename)
