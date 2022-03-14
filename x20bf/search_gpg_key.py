from logger import logger
from time_functions import btc_unix_time_millis


def search_gpg_key(gpg_key, api):
    # TODO: refactor asyncio
    try:
        global r
        request = api.request("search/tweets", {"q": gpg_key})
        try:
            with open(gpg_key + ":" + btc_unix_time_millis(), "w+") as f:
                f.write(request.text)
                f.close
        except Exception:
            logger.info("TRY GPGR FAILED!")
            pass
    except Exception:
        logger.info("GPGR SEARCH FAILED!")
        pass
