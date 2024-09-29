import os
from pathlib import Path

LEDS_INSTALL_CFG = os.environ.get("LEDS_INSTALL_CFG")

class GpioService():
    
    def __init__(self, pin, port, ledCount):
        self.pin = pin
        self.port = port
        self.ledCount = ledCount


class ConfigReader():

    configs = []

    @staticmethod
    def initConfigs(config):
        result = []
        services = config.split(":")
        for service in services:
            args = service.split(",")
            pin = None
            port = None
            ledCount = None
            for arg in args:
                keyValuePair = arg.split("=")
                if (len(keyValuePair) == 2):
                    key = keyValuePair[0]
                    value = keyValuePair[1]
                    
                    if (key == "pin"):
                        pin = value
                    elif (key == "port"):
                        port = value
                    elif (key == "ledCount"):
                        ledCount = value

            if (pin != None and port != None and ledCount != None):
                result.append(GpioService(pin, port, ledCount))

        if (len(result) == 0):
            result.append(GpioService("18", "9000", "10"))
        ConfigReader.configs = result

    @staticmethod
    def readCfgFile():
        path = Path(__file__).parent / "../config/install.cfg"
        data = ""
        if (path.is_file()):
            with path.open() as f:
                data = f.read().rstrip()
        return data
 
    @staticmethod
    def read():
        if (len(ConfigReader.configs) == 0):
            print("Reading install.config", end=" ")
            data = ""
            if not LEDS_INSTALL_CFG:
                data = ConfigReader.readCfgFile()
            else:
                data = LEDS_INSTALL_CFG
            print(" => "+data)
            ConfigReader.initConfigs(data)
        else:
            print("Returning existing loaded install.config")

        return ConfigReader.configs
