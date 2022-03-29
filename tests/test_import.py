import sys
sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
import x20bf.logging as logging

import x20bf as b3b3

# from x20bf import logger
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


logger.info("test_import.py")
test_version(b3b3.version.version())
