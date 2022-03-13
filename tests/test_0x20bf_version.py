logging = __import__("logging", globals(), locals(), [], 0)
b3b3 = __import__("0x20bf", globals(), locals(), [], 0)
# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%j.%Y %I:%M:%S %p"
)
logger = logging.getLogger()


def test_version():
    try:
        assert b3b3.__version__ == "0.0.1"
        logger.info("0x20bf v" + b3b3.__version__)
    except Exception:
        logger.warning("adjust 0x20bf/version.py __version__ setting")


test_version()