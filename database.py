import subprocess

class Database():
    
    @staticmethod
    def writeWeight(weight):
        influxLine = f"INSERT telemetry weight={weight}"
        
        subProcessOutput = subprocess.run(
            ['influx', '-database', 'sensors', '-execute', influxLine],
            stdout=subprocess.PIPE)
        
        return subProcessOutput.stderr
