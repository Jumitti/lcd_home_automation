try:
    from .i2c_dev import Lcd, CustomCharacters
except ModuleNotFoundError as e:
    print(f"{e}, you can use LCDSimulator and CustomCharactersSimulator instead")
from .simulator import LcdSimulator, CustomCharactersSimulator
