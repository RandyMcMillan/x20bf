#!/usr/bin/env python3
from configs import DATA_LOGGER, LOGGER
from TwitterAPI import TwitterAPI

from logger import logger
from time_functions import BTC_TIME, BTC_UNIX_TIME_MILLIS
from twitter_api_keys import AT, ATS, CAK, CASK

api = TwitterAPI(CAK, CASK, AT, ATS)
# if (LOGGER): print(api)


def set_old_block_time():
    f = open("OLD_BLOCK_TIME", "w")
    f.write(str(BTC_TIME()))
    f.close()


def get_old_block_time():
    f = open("OLD_BLOCK_TIME", "r")
    OBT = str(f.read())
    f.close()
    if DATA_LOGGER:
        logger.info(OBT)  # unsecure
    set_old_block_time()
    return OBT


def tweet_block_time():
    # print(BTC_TIME())
    # print(get_old_block_time())
    # print(int(BTC_TIME()) != int(get_old_block_time()))
    # set_old_block_time()
    if int(BTC_TIME()) != int(get_old_block_time()):
        request = api.request("statuses/update", {"status": BTC_UNIX_TIME_MILLIS()})
        if LOGGER:
            logger.info(request)
        if request.status_code == 200:
            logger.info("api.request SUCCESS")
        else:
            logger.info("api.request FAILURE")
    else:
        logger.info("tweetblock_time() FAILURE")


if __name__ == "__main__":

    tweet_block_time()
