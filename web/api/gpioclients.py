from config.configreader import ConfigReader
from api.commandclient import CommandClient

class GpioClients():

    commandClients = []

    @staticmethod
    def initialize():
        if (len(GpioClients.commandClients) == 0):
            result = []
            configs = ConfigReader.read()
            for i, config in enumerate(configs):
                result.append(CommandClient("localhost", config.port))
#               result.append(CommandClient("leds-"+str(i + 1), config.port))

            GpioClients.commandClients = result

    @staticmethod
    def get(index):
        if (index < 1 or index - 1 > len(GpioClients.commandClients)):
            index = 1
        return GpioClients.commandClients[index - 1]
