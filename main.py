import sys
import json
from src.raspberry_factory import RaspberryFactory
from src.audio_feedback import AudioFeedback
from src.config_loader import ConfigLoader
from src.scale_reader import ScaleReader
from src.database import Database
from src.weight_monitor import WeightMonitor


dry_run = "-d" in sys.argv or "--dry-run" in sys.argv
monitor = WeightMonitor(scale_reader=ScaleReader(ConfigLoader(json)),
                        audio_feedback=AudioFeedback(),
                        database=Database,
                        raspberry_factory=RaspberryFactory(),
                        delay=7,
                        dry_run=dry_run)
monitor.run()