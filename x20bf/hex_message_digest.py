import hashlib

from delimiter_stripper import delimiter_stripper
from logger import logger

LOGGER = True
HEX_LOGGER = False


def test_hash_lib_sha256():
    TEST_256 = hashlib.sha256()
    # empty string reserved for protocol
    assert TEST_256.digest_size == pow(2, 5)
    assert TEST_256.block_size == pow(2, 6)
    assert (
        TEST_256.hexdigest()
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    return TEST_256.hexdigest()


def test_hash_lib_ripemd160():
    TEST_160 = hashlib.new("ripemd160")
    assert TEST_160.digest_size == 20
    assert TEST_160.block_size == pow(2, 6)
    # empty string reserved for protocol
    assert TEST_160.hexdigest() == "9c1185a5c5e9fc54612808977ee8f548b2258d31"
    return TEST_160.hexdigest()


def hex_message_digest(recipient, message, sender):

    test_hash_lib_ripemd160()
    recipient = delimiter_stripper(recipient)
    message = delimiter_stripper(message)
    sender = delimiter_stripper(sender)

    n_160 = hashlib.new("ripemd160")
    # empty string reserved for protocol
    assert n_160.hexdigest() == test_hash_lib_ripemd160()

    if HEX_LOGGER:
        logger.info(str(":RIPEMD160:") + n_160.hexdigest() + str(":"))

    # RIPEMD160(RIPEMD160() + GPGR)
    n_160.update(bytes(recipient, "utf-8"))
    if HEX_LOGGER:
        logger.info(str(":RIPEMD160:") + n_160.hexdigest() + str(":"))

    # RIPEMD160(RIPEMD160(RIPEMD160() + GPGR) + message)
    n_160.update(bytes(message, "utf-8"))
    if HEX_LOGGER:
        logger.info(str(":RIPEMD160:") + n_160.hexdigest() + str(":"))

    # RIPEMD160(RIPEMD160(RIPEMD160() + GPGR) + message) + GPGS)
    n_160.update(bytes(sender, "utf-8"))
    if HEX_LOGGER:
        logger.info(str(":RIPEMD160:") + n_160.hexdigest() + str(":"))

    return n_160.hexdigest()


GPGR = "4DC9817F"  # bitkarrot
# logger.info(GPGR)
GPGS = "BB06757B"  # randymcmillan
# logger.info(GPGS)
MESSAGE = "text human readable message"
if HEX_LOGGER:
    logger.info(hex_message_digest(GPGR, MESSAGE, GPGS))
# hex_message_digest(GPGR, MESSAGE, GPGS)
