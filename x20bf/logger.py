#!/usr/bin/env python3
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%j.%Y %I:%M:%S %p"
)
logger = logging.getLogger()
