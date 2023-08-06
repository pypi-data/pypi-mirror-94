"""
Plugin for :py:mod:`puresnmp` to support AES-CFB-128bit encryption for SNMPv3

Implementation of the AES encryption ("usmAesCfb128PrivProtocol") according
to :rfc:`3826`
"""
from random import randint
from typing import Generator, NamedTuple

from Crypto.Cipher import AES

IDENTIFIER = "aes"
IANA_ID = 4


class EncryptionResult(NamedTuple):
    ciphertext: bytes
    salt: bytes


def pad_packet(data: bytes, block_size: int = 8) -> bytes:
    """
    Pads a packet to being a multiple of *block_size*.

    In x.690 BER encoding, the data contains length-information so
    "over-sized" data can be decoded without issue. This function simply adds
    zeroes at the end as needed.

    Packets also don't need to be "unpadded" for the same reason
    See https://tools.ietf.org/html/rfc3414#section-8.1.1.3

    >>> pad_packet(b"hello")
    b'hello\\x00\\x00\\x00'
    >>> pad_packet(b"hello123")
    b'hello123'
    """
    rest = len(data) % block_size
    if rest == 0:
        return data
    numpad = block_size - rest
    return data + numpad * b"\x00"


def reference_saltpot() -> Generator[int, None, None]:
    """
    Creates a new source for salt numbers.

    Following :rfc:`3414` this starts at a random number and increases on
    each subsequent retrieval.
    """
    salt = randint(1, 0xffffffffffffffff - 1)
    while True:
        yield salt
        salt += 1
        if salt == 0xffffffffffffffff:
            salt = 0


SALTPOT = reference_saltpot()


def get_iv(engine_boots: int, engine_time: int, local_salt: bytes) -> bytes:
    """
    See https://tools.ietf.org/html/rfc3826#section-3.1.2.1
    """
    # IV             = xxxxxxxxxxxxxxxx
    # | engine-boots = xxxx............ (big endian int)
    # | engine-time  = ....xxxx........ (big endian int)
    # | local_salt   = ........xxxxxxxx (big endian int)
    output = (
        engine_boots << (64 + 32)
        | engine_time << 64
        | int.from_bytes(local_salt, "big")
    )
    return output.to_bytes(16, "big")


def encrypt_data(
    localised_key: bytes,
    engine_id: bytes,
    engine_boots: int,
    engine_time: int,
    data: bytes,
) -> EncryptionResult:
    """
    See https://tools.ietf.org/html/rfc3826#section-3.1.3
    """
    salt = next(SALTPOT).to_bytes(8, "big")
    iv = get_iv(engine_boots, engine_time, salt)
    aes_key = localised_key[:16]
    cipher = AES.new(aes_key, AES.MODE_CFB, iv, segment_size=128)
    padded = pad_packet(data, 16)
    output = cipher.encrypt(padded)
    return EncryptionResult(output, salt)


def decrypt_data(
    localised_key: bytes,
    engine_id: bytes,
    engine_boots: int,
    engine_time: int,
    salt: bytes,
    data: bytes,
) -> bytes:
    """
    See https://tools.ietf.org/html/rfc3826#section-3.1.4
    """
    iv = get_iv(engine_boots, engine_time, salt)
    aes_key = localised_key[:16]
    cipher = AES.new(aes_key, AES.MODE_CFB, iv, segment_size=128)
    padded = pad_packet(data, 16)
    output = cipher.decrypt(padded)
    return output
