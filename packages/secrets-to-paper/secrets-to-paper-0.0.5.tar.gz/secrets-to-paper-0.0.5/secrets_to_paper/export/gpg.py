import subprocess
from secrets_to_paper.export.qr import get_qr_codes
from secrets_to_paper.export import templateEnv, templateLoader, write_pdf_to_disk
import subprocess
import base64
import os
import io
import errno
import jinja2
import qrcode
from PIL import Image
from itertools import zip_longest
import datetime


def render_gpg_html(
    paperkey_b16,
    ascii_key,
    qr_images=[],
    public_qr_images=[],
    public_key_ascii="",
    key_id="",
    timestamp=None,
):

    template = templateEnv.get_template("gpg_key.html")

    rendered = template.render(
        qr_images=qr_images,
        paperkey_b16=paperkey_b16,
        ascii_key=ascii_key,
        public_key_ascii=public_key_ascii,
        key_id=key_id,
        public_qr_images=public_qr_images,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    )

    return rendered


def export_gpg(key_id):
    """
    Export a gpg key using the paperkey subcommand
    """

    secret = subprocess.run(["gpg", "--export-secret-key", key_id], capture_output=True)
    secret_key_ascii = subprocess.run(
        ["gpg", "--export-secret-key", "--armor", key_id], capture_output=True
    ).stdout.decode("ascii")

    public_key = subprocess.run(
        ["gpg", "--export", "--armor", key_id], capture_output=True
    ).stdout
    public_qr_codes = get_qr_codes(public_key)

    # used for producing QR codes (paperkey pulls relevant secret bits)
    paperkey_raw = subprocess.run(
        ["paperkey", "--output-type", "raw"], input=secret.stdout, capture_output=True
    )
    qr_codes = get_qr_codes(base64.b64encode(paperkey_raw.stdout))

    # used for produces textual output
    paperkey = subprocess.run(
        ["paperkey", "--output-type", "base16"],
        input=secret.stdout,
        capture_output=True,
    )
    paperkey_output = paperkey.stdout.decode("utf-8")

    filename = key_id + ".pdf"

    rendered = render_gpg_html(
        paperkey_output,
        secret_key_ascii,
        public_key_ascii=public_key.decode("ascii"),
        qr_images=qr_codes,
        public_qr_images=public_qr_codes,
        key_id=key_id,
    )

    write_pdf_to_disk(rendered, filename)
