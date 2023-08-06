from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    PublicFormat,
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateNumbers,
    RSAPublicNumbers,
    rsa_crt_iqmp,
    rsa_crt_dmp1,
    rsa_crt_dmq1,
)


def generate_rsa_key(public_key_path, p, q, n, e):

    with open(public_key_path) as public_key:

        pubkey = serialization.load_pem_public_key(
            public_key.read().encode("ascii"), backend=default_backend()
        )

    # a lot of software (including openssl) expects p to be the larger prime
    # instead of expecting the user to get it right, just reassign them here
    p, q = sorted((p, q))
    q = int(q, 16)
    p = int(p, 16)

    e = pubkey.public_numbers().e
    n = pubkey.public_numbers().n

    # private exponent
    d = int(pow(e, -1, (p - 1) * (q - 1)))

    dmp1 = rsa_crt_dmp1(d, p)
    dmq1 = rsa_crt_dmq1(d, q)
    iqmp = rsa_crt_iqmp(p, q)

    priv_nums = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, pubkey.public_numbers())
    priv_key = priv_nums.private_key(default_backend())

    pem = priv_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption(),
    )

    print(pem.decode("ascii"))
