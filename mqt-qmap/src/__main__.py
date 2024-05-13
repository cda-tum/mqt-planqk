from __future__ import annotations

import json
import locale
import logging
import os
import sys
from pathlib import Path

from loguru import logger

from .libs.logging_util import LogHandler
from .program import run

logging_level = os.environ.get("LOG_LEVEL", "DEBUG")
logging.getLogger().handlers = [LogHandler()]
logging.getLogger().setLevel(logging_level)
logger.configure(handlers=[{"sink": sys.stdout, "level": logging_level}])

with Path("./input/data.json").open(encoding=locale.getpreferredencoding(False)) as file:
    data = json.load(file)

with Path("./input/params.json").open(encoding=locale.getpreferredencoding(False)) as file:
    params = json.load(file)

response = run(data, params)

print()
print(response.to_json())
