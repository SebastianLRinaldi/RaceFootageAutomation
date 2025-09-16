from typing import Protocol, List

from .structure_interface import StructureInterface
from PyQt6.QtWidgets import QWidget

class ComponentInterface(Protocol):
    structure: StructureInterface    # your existing interface
    logic: object                   # could be a LogicInterface if you define one
    connection: object              # could be a ConnectionsInterface