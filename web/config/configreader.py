from pathlib import Path

class GpioService():
    
    def __init__(self, pid, port, ledCount):
        self.pid = pid
        self.port = port
        self.ledCount = ledCount


class ConfigReader():

    configs = []

    @staticmethod
    def parseString(config):
        result = []
        services = config.split(":")
        for service in services:
            args = service.split(",")
            pid = None
            port = None
            ledCount = None
            for arg in args:
                keyValuePair = arg.split("=")
                if (len(keyValuePair) == 2):
                    key = keyValuePair[0]
                    value = keyValuePair[1]
                    
                    if (key == "pid"):
                        pid = value
                    elif (key == "port"):
                        port = value
                    elif (key == "ledCount"):
                        ledCount = value

            if (pid != None and port != None and ledCount != None):
                result.append(GpioService(pid, port, ledCount))

        if (len(result) == 0):
            result.append(GpioService("18", "9000", "10"))
        ConfigReader.configs = result

    @staticmethod
    def read():
        if (len(ConfigReader.configs) == 0):
            print("Reading install.config")
            path = Path(__file__).parent / "../config/install.cfg"
            data = ""
            if (path.is_file()):
                with path.open() as f:
                    data = f.read().rstrip()
            ConfigReader.parseString(data)
        else:
            print("Returning existing loaded install.config")

        return ConfigReader.configs
