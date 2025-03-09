from enum import Enum

class TokenType(Enum):
  BEGIN = 1
  END = 2
  LOGICAL_OPERATION = 3
  ARITHMETIC_OPERATION = 4
  VARIABLE = 5
  END_LINE = 6
  FUNCTION = 7
  DEFINITION = 8
  BUILT_IN_FUNCTIONS = 9
  VALUE = 10
  UNKNOWN = 11

class BuiltInFunction(Enum):
  PRINT = 1
  SIN = 2
  COS = 3

class ArithmeticOperation(Enum):
  ASSIGN = 1
  PLUS = 2
  MINUS = 3
  DIVISION = 4
  MULTIPLICATION = 5

class LogicalOperation(Enum):
  NOT = 1
  OR = 2
  AND = 3
  EQUALS = 4
  MORE = 5
  LESS = 6
  LESS_EQ = 7
  MORE_EQ = 8
  NOT_EQ = 9

class ValueType(Enum):
  STRING = 1
  INT = 2
  FLOAT = 3
