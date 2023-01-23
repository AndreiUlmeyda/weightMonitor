# pylint: disable=R0903
"""
Simple module to provide write access to a local database.
"""

import subprocess


class Database:
    """
    Allow writing to a local InfluxDB using the command line interface.
    """
    def __init__(self):
        self.database_name = 'sensors'
        self.measurement_name = 'telemetry'
        self.field_name = 'weight'

    def write_weight(self, weight):
        """
        Assume database name, measurement name etc. and use a subprocess
        to call the InfluxDB command line tool.
        """
        influx_line = f"INSERT {self.measurement_name} {self.field_name}={weight}"

        subprocess_output = subprocess.run([
            'influx', '-database', self.database_name, '-execute', influx_line
        ],
                                           stdout=subprocess.PIPE,
                                           check=True)

        return subprocess_output.stderr
