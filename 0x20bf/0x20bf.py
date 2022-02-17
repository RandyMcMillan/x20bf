#!/usr/bin/env python3
import argparse
import configparser
import hashlib
import sys

import psutil

# from search_gpg_key import search_gpg_key
# from time_functions import btc_time, unix_time_millis
import time_functions as tf
from delimiter_stripper import delimiter_stripper
from logger import logger

# import os

# from TwitterAPI import TwitterAPI

# from TwitterAPI import TwitterAPI


global user
global is_macos
global is_linux
global is_windows
user = psutil.Process().username()
is_macos = psutil.MACOS
is_linux = psutil.LINUX
# windows support not planned - but PRs are welcome
is_windows = psutil.WINDOWS

# Setup logging
global logger
global os_logger
global data_logger
global hex_logger
global genesis_time
global time_logger
global mempool_logger

# global variables
# we leave comments in PROTOCOL format ie. GPGR DIGEST etc...
global HEADER
global DIGEST
global BODY
global DATA
global TEST_256
global GPGR
global GPGS
global MESSAGE
global GOLDEN_RATIO

global tweet

# # REF: https://docs.python.org/3/library/configparser.html
#
# # get the path to config.ini
# sys.path.insert(0, '.')
# sys.path.insert(1, '0x20bf')
# sys.path.insert(2, '../0x20bf')
# config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
#
# # check if the path is to a valid file
# if not os.path.isfile(config_path):
#     print('BadConfigError')  # not a standard python exception
#
# config = configparser.ConfigParser()
# config.read(config_path)
# # config.read("configs.ini")
# config.sections()
# config.get("DEFAULTS", "", fallback=False)
#
#
# if config.getboolean("DEFAULTS", "tweet"):
#     twitter_api = configparser.ConfigParser()
#     twitter_api.read("configs.ini")
#     twitter_api.sections()
#     twitter_api.get("twitter", "", fallback=0)
#     AT = twitter_api.get("twitter", "access_token")
#     ATS = twitter_api.get("twitter", "access_token_secret")
#     CAK = twitter_api.get("twitter", "consumer_api_key")
#     CASK = twitter_api.get("twitter", "consumer_api_secret_key")
#     api = TwitterAPI(CAK, CASK, AT, ATS)


def test_hash_lib():
    TEST_256 = hashlib.sha256()
    # empty string reserved for protocol
    assert TEST_256.digest_size == pow(2, 5)
    assert TEST_256.block_size == pow(2, 6)
    assert (
        TEST_256.hexdigest()
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    return TEST_256.hexdigest()


def HEX_MESSAGE_TREE(recipient, sender):
    recipient = delimiter_stripper(recipient)
    sender = delimiter_stripper(sender)

    n_256 = hashlib.sha256()
    logger.info("n_256:")
    logger.info(n_256.hexdigest())
    # empty string reserved for protocol
    assert n_256.hexdigest() == test_hash_lib()

    # SHA256() + GPGR
    n_256.update(bytes(recipient, "utf-8"))
    # if (hex_logger): logger.info(n_256.digest())
    logger.info("n_256 + recipient:")
    logger.info(n_256.hexdigest())
    # if (hex_logger): logger.info(n_256.digest_size)
    # if (hex_logger): logger.info(n_256.block_size)

    # SHA256() + GPGR+GPGS
    n_256.update(bytes(sender, "utf-8"))
    # if (hex_logger): logger.info(n_256.digest())
    # if (hex_logger): logger.info(n_256.hexdigest())
    # if config.getboolean("DEFAULTS", "hex_logger"):
    logger.info("n_256 + recipient+sender:")
    logger.info(n_256.hexdigest())
    # if (hex_logger): logger.info(n_256.digest_size)
    # if (hex_logger): logger.info(n_256.block_size)

    # TODO: populate message tree
    # if config.getboolean("DEFAULTS", "hex_logger"):
    logger.info(n_256.hexdigest())

    return n_256.hexdigest()


def HEX_MESSAGE_DIGEST(recipient, message, sender):
    recipient = delimiter_stripper(recipient)
    sender = delimiter_stripper(sender)
    message = delimiter_stripper(message)

    n_256 = hashlib.sha256()
    # empty string reserved for protocol
    assert n_256.hexdigest() == test_hash_lib()

    # SHA256() + GPGR
    n_256.update(bytes(recipient, "utf-8"))
    logger.info(n_256.hexdigest())

    # SHA256() + GPGR+MESSAGE
    n_256.update(bytes(message, "utf-8"))
    logger.info(n_256.hexdigest())

    # SHA256() + GPGR+MESSAGE+GPGS
    n_256.update(bytes(sender, "utf-8"))
    logger.info(n_256.hexdigest())

    # TODO: populate message tree
    logger.info(n_256.hexdigest())

    return n_256.hexdigest()


def message_header():
    # the HEADER is prepended with GPGR
    # the HEADER is appended with GPGS
    DIGEST = HEX_MESSAGE_DIGEST(GPGR, MESSAGE, GPGS)
    LOC = (
        "https://github.com/0x20bf-org/0x20bf/blob/main/"
        + GPGR
        + DIGEST
        + str(tf.btc_time())
        + str(tf.unix_time_millis())
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
        + str(tf.btc_time())
        + ":"
        + str(tf.unix_time_millis())
        + ":"
        + GPGS
        + ":"
        + LOC
        + ":"
    )

    if logger:
        logger.info(HEADER)
    # HEADER_STRUCTURE = str(":GPGR:DIGEST:btc_time:unix_time_millis:GPGS:LOC:")
    return HEADER


def send_message(tweet, api):
    header = message_header()
    # body = message_body()
    if logger:
        logger.info(header)
    if tf.btc_time() != 0:
        if tweet:
            request = api.request("statuses/update", {"status": header})
            if request.status_code == 200:
                logger.info("api.request SUCCESS")
            else:
                logger.info("api.request FAILURE")
        else:
            logger.info("tweet=" + str(tweet))
    else:
        logger.info("tweetblock_time() FAILURE")


# logger.info(BTC_unix_time_millis())

GPGR = "4DC9817F"  # bitkarrot
logger.info(GPGR)
GPGS = "BB06757B"  # randymcmillan
logger.info(GPGS)
MESSAGE = "text human readable message"


def log_os():
    if is_macos:
        logger.info(str("is_macos"))

    if is_linux:
        logger.info(str("is_linux"))

    if is_windows:
        logger.info(str("is_windows"))


def main(args):
    # parse values from a configuration file if provided and use those as the
    # default values for the argparse arguments
    config_argparse = argparse.ArgumentParser(prog=__file__, add_help=False)
    config_argparse.add_argument(
        "-c", "--config-file", help="path to configuration file"
    )
    config_args, _ = config_argparse.parse_known_args(args)

    defaults = {
        "default_port": 8383,
        "tweet": False,
        "text_message": False,
        "search": False,
        "logger": False,
        "os_logger": True,
        "data_logger": False,
        "hex_logger": False,
        "time_logger": False,
        "mempool_logger": False,
        "option1": False,
        "option2": False,
    }

    if config_args.config_file:
        logger.info("Loading configuration: {}".format(config_args.config_file))
        try:
            config_parser = configparser.ConfigParser()
            with open(config_args.config_file) as f:
                config_parser.read_file(f)
            config_parser.read(config_args.config_file)
        except OSError as err:
            logger.error(str(err))
            sys.exit(1)

        defaults.update(dict(config_parser.items("options")))

    # parse the program's main arguments using the dictionary of defaults and
    # the previous parsers as "parent' parsers
    parsers = [config_argparse]
    main_parser = argparse.ArgumentParser(prog=__file__, parents=parsers)
    main_parser.set_defaults(**defaults)

    # args still need to be set up
    main_parser.add_argument("-dp", "--default_port")
    main_parser.add_argument("-l", "--logger")
    main_parser.add_argument("-ol", "--os_logger")
    main_parser.add_argument("-dl", "--data_logger")
    main_parser.add_argument("-hl", "--hex_logger")
    main_parser.add_argument("-tl", "--time_logger")
    main_parser.add_argument("-mpl", "--mempool_logger")
    main_parser.add_argument("-s", "--search")
    main_parser.add_argument("-t", "--tweet")
    main_parser.add_argument("-1", "--option1")
    main_parser.add_argument("-2", "--option2")
    main_parser.add_argument("-tm", "--text_message")
    main_args = main_parser.parse_args(args)
    print(main_args.option1)
    print(main_args.option2)
    print(main_args.logger)
    print(main_args.tweet)
    if main_args:
        tweet = main_args.tweet
        logger.info(tweet)
        text_message = main_args.text_message
        logger.info(text_message)
        mempool_logger = main_args.mempool_logger
        logger.info(mempool_logger)
        hex_logger = main_args.hex_logger
        if hex_logger:
            logger.info(HEX_MESSAGE_DIGEST(GPGR, MESSAGE, GPGS))
            HEX_MESSAGE_TREE(GPGR, GPGS)
            HEX_MESSAGE_DIGEST(GPGR, MESSAGE, GPGS)


if __name__ == "__main__":
    GPGR = "4DC9817F"  # bitkarrot
    logger.info(GPGR)
    GPGS = "BB06757B"  # randymcmillan
    logger.info(GPGS)
    MESSAGE = "text human readable message"
    main(sys.argv[1:])
