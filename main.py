"""
This is a console application used to read values
off of a bathroom scale and store them in a database.
Some audio feedback is provided during the process.

There is a single command line flag:

-d or --dry-run

When this flag is set nothing will be written
to the database.
"""

import sys
import os
import json
import logging

from src.raspberry_factory import RaspberryFactory
from src.audio_feedback import AudioFeedback
from src.config_loader import ConfigLoader
from src.scale_reader import ScaleReader
from src.database import Database
from src.weight_monitor import WeightMonitor

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

os.system('clear')
logging.info('Preparing...')

dry_run = "-d" in sys.argv or "--dry-run" in sys.argv

monitor = WeightMonitor(scale_reader=ScaleReader(ConfigLoader(json)),
                        audio_feedback=AudioFeedback(),
                        database=Database,
                        raspberry_factory=RaspberryFactory(),
                        delay=7,
                        dry_run=dry_run)

monitor.run()
