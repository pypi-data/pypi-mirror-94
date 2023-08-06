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


templateLoader = jinja2.PackageLoader("secrets_to_paper", "templates")
templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True)

def write_pdf_to_disk(rendered_html, output_file):

    html = HTML(string=rendered_html)
    css = templateEnv.get_template("main.css").render()

    css = CSS(string=css)

    html.write_pdf(
        output_file, stylesheets=[css],
    )

    return None
