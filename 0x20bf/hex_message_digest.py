import hashlib

from delimiter_stripper import delimiter_stripper
from logger import logger
from time_functions import btc_time, unix_time_millis

LOGGER = True
HEX_LOGGER = True


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
    # if HEX_LOGGER:
    #     logger.info(TEST_160.hexdigest())
    #     logger.info(str(TEST_160.digest_size))
    #     logger.info(str(TEST_160.block_size))
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


def message_header():
    # the HEADER is prepended with GPGR
    # recipient comes first - GPGR
    # the HEADER is appended with GPGS then lastly LOC (location)
    # HEADER_STRUCTURE = str(":GPGR:DIGEST:BTC_TIME:UNIX_TIME_MILLIS:GPGS:LOC:")
    DIGEST = hex_message_digest(GPGR, MESSAGE, GPGS)
    # TODO GPGR short gpg id determines the branch of the repo
    # the GPGR short id name space will be shared with nodes
    # share_public_keyring() will trigger a node to exchange
    # AFTER it has been interogated and verified
    # upon git_request(GPGR) - tbd
    LOC = (
        "https://github.com/0x20bf-org/0x20bf/blob/"
        + GPGR
        + DIGEST
        + btc_time()
        + unix_time_millis()
        + GPGS
        + ".txt.gpg"
    )
    # LOC is appended on to DIGEST
    HEADER = str(
        ":"
        + GPGR
        + ":"
        + DIGEST
        + ":"
        + btc_time()
        + ":"
        + unix_time_millis()
        + ":"
        + GPGS
        + ":"
        + LOC
        + ":"
    )

    if LOGGER:
        logger.info(HEADER)
    # HEADER_STRUCTURE = str(":GPGR:DIGEST:BTC_TIME:UNIX_TIME_MILLIS:GPGS:LOC:")
    return HEADER


# logger.info(BTC_UNIX_TIME_MILLIS())

GPGR = "4DC9817F"  # bitkarrot
# logger.info(GPGR)
GPGS = "BB06757B"  # randymcmillan
# logger.info(GPGS)
MESSAGE = "text human readable message"
# if HEX_LOGGER:
# logger.info(hex_message_digest(GPGR, MESSAGE, GPGS))
hex_message_digest(GPGR, MESSAGE, GPGS)
