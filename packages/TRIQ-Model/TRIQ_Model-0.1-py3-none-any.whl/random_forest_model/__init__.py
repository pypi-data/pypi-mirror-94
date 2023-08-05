import logging

from random_forest_model.config.core import PACKAGE_ROOT

logging.getLogger(__name__).addHandler(logging.NullHandler())


with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()
