from enum import Enum


class EditorType(Enum):
    Manual = -1
    Text = 0
    JSON = 1
    XML = 2
    HTML = 3
    Javascript = 4


class ParamType(Enum):
    JSON = 0
    Param = 1
    XML = 2
    Table = 3
