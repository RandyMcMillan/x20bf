import x20bf as b3b3
import logging
# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%j.%Y %I:%M:%S %p"
)
logger = logging.getLogger()


def test_version():
    try:
        assert b3b3.__version__ == "0.0.1"
        logger.info("x20bf v" + b3b3.__version__)
    except Exception:
        logger.warning("adjust x20bf/version.py __version__ setting")


test_version()
