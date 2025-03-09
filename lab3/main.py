from TokenType import *
from Tokeniser import *

tokenMap = {
  "begin": TokenType.BEGIN,
  "end": TokenType.END,
  ";": TokenType.END_LINE,
  "(": TokenType.BRACKETS,
  ")": TokenType.BRACKETS,
  "{": TokenType.BRACKETS,
  "}": TokenType.BRACKETS,
  "[": TokenType.BRACKETS,
  "]": TokenType.BRACKETS,
  "=": TokenType.ARITHMETIC_OPERATION,
  "+": TokenType.ARITHMETIC_OPERATION,
  "-": TokenType.ARITHMETIC_OPERATION,
  "/": TokenType.ARITHMETIC_OPERATION,
  "*": TokenType.ARITHMETIC_OPERATION,
  "!": TokenType.LOGICAL_OPERATION,
  "||": TokenType.LOGICAL_OPERATION,
  "&&": TokenType.LOGICAL_OPERATION,
  "==": TokenType.LOGICAL_OPERATION,
  ">": TokenType.LOGICAL_OPERATION,
  "<": TokenType.LOGICAL_OPERATION,
  "<=": TokenType.LOGICAL_OPERATION,
  ">=": TokenType.LOGICAL_OPERATION,
  "!=": TokenType.LOGICAL_OPERATION,
}

# Add built-in functions
for func in BuiltInFunction:
  tokenMap[func.name.lower()] = TokenType.BUILT_IN_FUNCTIONS

# Add arithmetic operations
arithmetic_ops = {
  "=": ArithmeticOperation.ASSIGN,
  "+": ArithmeticOperation.PLUS,
  "-": ArithmeticOperation.MINUS,
  "/": ArithmeticOperation.DIVISION,
  "*": ArithmeticOperation.MULTIPLICATION,
}
for op, type_enum in arithmetic_ops.items():
  tokenMap[op] = TokenType.ARITHMETIC_OPERATION

# Add logical operations
logical_ops = {
  "!": LogicalOperation.NOT,
  "||": LogicalOperation.OR,
  "&&": LogicalOperation.AND,
  "==": LogicalOperation.EQUALS,
  ">": LogicalOperation.MORE,
  "<": LogicalOperation.LESS,
  "<=": LogicalOperation.LESS_EQ,
  ">=": LogicalOperation.MORE_EQ,
  "!=": LogicalOperation.NOT_EQ,
}
for op, type_enum in logical_ops.items():
  tokenMap[op] = TokenType.LOGICAL_OPERATION

tokeniser = Tokeniser(tokenMap)

[print (i) for i in tokeniser.tokenize("begin if (+ 10 == 11); ifElse/11 != print(anton) sin cos end")]