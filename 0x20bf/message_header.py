#!/usr/bin/env python3
from hex_message_digest import hex_message_digest
from logger import logger
from time_functions import btc_time, unix_time_millis

LOGGER = True
HEX_LOGGER = True


def message_header(GPGR, MESSAGE, GPGS, LOC):
    # the HEADER is prepended with GPGR
    # the HEADER is appended with GPGS
    DIGEST = hex_message_digest(GPGR, MESSAGE, GPGS)
    if LOGGER:
        logger.info(DIGEST)
    # TODO branch will be dynamic based on message tree - tbd
    # LOC isnt nesseccsarally a web asset
    # LOC is just a string - maybe a geo location for example
    BRANCH = "main"
    LOC = "https://github.com/0x20bf-org/0x20bf/blob/" + BRANCH
    # LOC is appended on to DIGEST
    HEADER = str(
        ":"
        + GPGR
        + ":"
        + DIGEST
        + ":"
        + str(btc_time())
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
    # ":GPGR:DIGEST:btc_time:unix_time_millis:GPGS:LOC:"
    return HEADER


def test_message_header():
    logger.info("test_message_header()")
    GPGR = "4DC9817F"  # bitkarrot
    logger.info(GPGR)
    GPGS = "BB06757B"  # randymcmillan
    logger.info(GPGS)
    MESSAGE = "text human readable message"
    if HEX_LOGGER:
        logger.info(hex_message_digest(GPGR, MESSAGE, GPGS))
    logger.info(str(message_header(GPGR, MESSAGE, GPGS, "test/location")))
    return message_header(GPGR, MESSAGE, GPGS, "test/location")


logger.info(test_message_header())
