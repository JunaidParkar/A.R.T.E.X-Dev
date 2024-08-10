from .i import Initiator
from .p import Packer
from .al import AddLibrary

class Studio:

    def __init__(self, cwd) -> None:
        self.__initiator = Initiator(cwd)
        self.__packer = Packer(cwd)
        self.__add_library = AddLibrary(cwd)

    def init(self):
        self.__initiator.initialize()

    def build(self):
        self.__packer.builder()