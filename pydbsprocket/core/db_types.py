from enum import Enum


class DataType(Enum):
    """Provider-agnostic data types"""
    INTEGER = "integer"
    BIGINT = "bigint"
    TEXT = "text"
    VARCHAR = "varchar"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DECIMAL = "decimal"
    TIMESTAMP = "timestamp"
    TIMESTAMPTZ = "timestamptz"
    DATE = "date"
    CURSOR = "refcursor"
    UUID = "uuid"

#BaseClass - For making operation in providers easier
class Param:
    def __init__(self, value, data_type: DataType|str):
        self._value = value
        self.type = data_type
    
    @property
    def value(self):
        return self._value
        
class OutputParameter(Param):
    def __init__(self, data_type:DataType):
        super().__init__(value=None, data_type=data_type)
    
class InputCollectionParameter(Param):
    def __init__(self, value, data_type: DataType|str):
        super().__init__(value=value, data_type=data_type)
        
