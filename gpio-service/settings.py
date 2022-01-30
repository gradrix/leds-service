import pickle

class Settings: 

    def __init__(self):
        self.loadDefaults()

    def loadDefaults(self):
        self.brightness = 0
        self.isOn = None
        self.mode = 0
        self.toggle = 0
        self.speed = 0
        self.color = ""
        self.ledCount = 0

    def reset(self):
        self.loadDefaults() 
        self.saveToFile()
    
    def saveToFile(self):
        try:
            with open("saved-data", "wb") as fi:
                settingsDict = {}
                settingsDict["brightness"] = self.brightness
                settingsDict["isOn"] = self.isOn
                settingsDict["mode"] = self.mode
                settingsDict["toggle"] = self.toggle
                settingsDict["speed"] = self.speed
                settingsDict["color"] = self.color
                pickle.dump(settingsDict, fi, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("Error while trying to save led settings: "+str(e))

    def openFromFile(self):
        try:
            with open("saved-data", "rb") as inp:
                loadedSettings = pickle.load(inp)
                self.brightness = loadedSettings["brightness"]
                self.isOn = loadedSettings["isOn"]
                self.mode = loadedSettings["mode"]
                self.toggle = loadedSettings["toggle"]
                self.speed = loadedSettings["speed"]
                self.color = loadedSettings["color"]
        except Exception as e:
            print("Error while loading saved data: "+str(e))
            self.brightness = 2
            self.isOn = True
            self.mode = 0
            self.toggle = 0
            self.speed = 4
            self.color = ""               
            self.saveToFile()
