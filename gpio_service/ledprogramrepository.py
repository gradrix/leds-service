import importlib
import inspect
import os
import glob

from gpio_service.common.ledprogrambase import LedProgramBase

LED_PROGRAMS_DIR = "ledprograms"


class ModeLayout:
    def __init__(self, modeIndex, modes):
        self.modeIndex = modeIndex
        self.minSpeed = 0
        self.maxSpeed = 100
        self.modes = modes


class LedProgramRepository:
    """Finds the programs in ledprograms/ and tracks the current one."""

    def __init__(self, settings, leds):
        self.settings = settings
        programs = [programType(settings, leds) for programType in self.findProgramTypes()]
        indexes = [program.modeIndex for program in programs]
        if len(set(indexes)) != len(indexes):
            raise ValueError("Two led programs share a modeIndex: " + str(sorted(indexes)))
        self.programs = {program.modeIndex: program for program in sorted(programs, key=lambda p: p.modeIndex)}
        print("Led programs: " + ", ".join(p.modeName for p in self.programs.values()))

        if settings.mode not in self.programs:
            settings.mode = min(self.programs)
        self.currentProgram = self.programs[settings.mode]

    def changeMode(self, newMode):
        """Returns False when no such program exists."""
        if newMode not in self.programs:
            return False
        self.settings.mode = newMode
        self.currentProgram = self.programs[newMode]
        return True

    def getModeLayout(self):
        return ModeLayout(self.currentProgram.modeIndex, list(self.programs.values()))

    def findProgramTypes(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), LED_PROGRAMS_DIR)
        found = []
        for path in glob.glob(os.path.join(directory, "*.py")):
            name = os.path.splitext(os.path.basename(path))[0]
            if name.startswith("__"):
                continue
            module = importlib.import_module("gpio_service." + LED_PROGRAMS_DIR + "." + name)
            for _, value in inspect.getmembers(module, inspect.isclass):
                if issubclass(value, LedProgramBase) and not inspect.isabstract(value):
                    found.append(value)
        return found
