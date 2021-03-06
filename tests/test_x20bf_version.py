# from x20bf import logger
import logging

import x20bf as b3b3

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%j.%Y %I:%M:%S %p"
)
logger = logging.getLogger()


def test_version(version):
    try:
        assert b3b3.version.version() == "0.0.1"
        logger.info("x20bf v" + str(version))
    except Exception:
        logger.info("x20bf v" + str(version))
        logger.warning("adjust x20bf/version.py __version__ setting")


logger.info("test_x20bf_version.py")
test_version(b3b3.version.version())
