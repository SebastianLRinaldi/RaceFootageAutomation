from typing import Protocol, List


class StructureInterface(Protocol):
    layout_data: List[str]  # type of data your layout builder consumes