logging = __import__("logging", globals(), locals(), [], 0)
b3b3 = __import__("0x20bf", globals(), locals(), ['version'], 0)
# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%j.%Y %I:%M:%S %p"
)
logger = logging.getLogger()


def test_version(version):
    try:
        assert b3b3.version.version() == "0.0.1"
        logger.info("0x20bf v" + str(version))
    except Exception:
        logger.info("0x20bf v" + str(version))
        logger.warning("adjust 0x20bf/version.py __version__ setting")


logger.info("test_0x20bf_version.py")
test_version(b3b3.version.version())
