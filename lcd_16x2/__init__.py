
try:
    from .drivers.i2c_dev import Lcd, CustomCharacters
except ModuleNotFoundError as e:
    print(f"{e}, you can use LCDEmulator and CustomCharactersEmulator instead")

from .emulators.emulator import LcdEmulator, CustomCharactersEmulator

__all__ = ["Lcd", "CustomCharacters", "LcdEmulator", "CustomCharactersEmulator"]

__version__ = "0.1.0-alpha3"
