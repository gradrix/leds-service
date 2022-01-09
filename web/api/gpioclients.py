import os
from config.configreader import ConfigReader
from api.commandclient import CommandClient

GPIO_SERVICE_HOST = os.environ.get("GPIO_SERVICE_HOST")

class GpioClients():

    commandClients = []

    @staticmethod
    def initialize():
        
        if (len(GpioClients.commandClients) == 0):
            result = []
            configs = ConfigReader.read()
            for i, config in enumerate(configs):
                if not GPIO_SERVICE_HOST:
                    result.append(CommandClient("localhost", config.port))
                else:
                    result.append(CommandClient(str(GPIO_SERVICE_HOST)+str(i + 1), config.port))

            GpioClients.commandClients = result

    @staticmethod
    def get(index):
        if (index < 1 or index - 1 > len(GpioClients.commandClients)):
            index = 1
        return GpioClients.commandClients[index - 1]
