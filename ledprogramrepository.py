import importlib
import inspect
import os
import glob
from abc import ABC
from LedPrograms.ledprogrambase import LedProgramBase

LED_PROGRAMS_DIR = "LedPrograms"

class LedProgramRepository:

  def __init__(self, settings, leds):
    self.programs = {}
    self.settings = settings
    programTypes = self.importFromFolder(LED_PROGRAMS_DIR, LedProgramBase)
    print("Initializing Led Programs: ", end = "")
    for programType in programTypes:
      print(str(programType.__name__), end = ", ")
      self.add(programType(settings, leds))
    print(" <- Success!")  

    programList = list(self.programs.items())
    programList.sort()
    self.programs = dict(programList)

  def show(self):
    mode = self.settings.mode
    if (mode in self.programs):
      self.programs[mode].show()
    else:
      self.settings.mode = self.tryChangeMode(0)
  
  def tryChangeMode(self, newMode):
    isNext = true if self.mode < newMode else false
    if (isNext):
      for i in range(newMode, max(self.programs, key=int)):
        if (i in self.programs):
          return i
    else:
      for i in range(min(self.programs, key=int), newMode):
        if (i in self.programs):
          return i

  def add(self, ledProgram):
    if (ledProgram.modeIndex in self.programs):
      raise ValueError("Error. LedProgram of index '"+str(ledProgram.modeIndex)+"' already exists in LedProgramRepository")
    self.programs[ledProgram.modeIndex] = ledProgram
    
  def importFromFolder(self, directoryPath, baseClass=None, filterAbstract=True):
    
    programTypes = []
    currentDir = os.path.dirname(os.path.abspath(__file__))
    dirPath = os.path.join(currentDir, directoryPath)
    packageName = os.path.basename(directoryPath)

    # -----------------------------
    # Iterate all python files within that directory
    filePaths = glob.glob(os.path.join(dirPath, "*.py"))
    for filePath in filePaths:
      programFileName = os.path.basename(filePath)

      className = os.path.splitext(programFileName)[0]

      if className.startswith("__"):
        continue

      # -----------------------------
      # Import python file
      module = importlib.import_module("." + className, package=packageName)

      # -----------------------------
      # Iterate items inside imported python file
      for item in dir(module):
        value = getattr(module, item)
        if not value:
          continue

        if not inspect.isclass(value):
          continue

        if filterAbstract and inspect.isabstract(value):
          continue

        if baseClass is not None:
          if type(value) != type(baseClass):
            continue
          
        if value.__name__ == ABC.__name__:
          continue
        
        programTypes.append(value)

    return programTypes