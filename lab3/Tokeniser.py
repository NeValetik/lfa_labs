from Token import *
from TokenType import *
import re

class Tokeniser:
  def __init__(self, tokenMap: dict[str, TokenType]):
      self.tokenMap = tokenMap

  def tokenize(self, text: str):
      tokenlist = []

      token_patterns = [
          (r'(!=|<=|>=|&&|==|\|\|)', TokenType.LOGICAL_OPERATION),  # Two-character logical operators
          (r'[\+\-\*/=]', TokenType.ARITHMETIC_OPERATION),       # Arithmetic operators
          (r'[0-9]+\.[0-9]+', TokenType.VALUE),                  # Float values
          (r'"[^"]*"', TokenType.VALUE),                         # String values
          (r'[0-9]+', TokenType.VALUE),                          # Integer values
          (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.VARIABLE),       # Variables
          (r'[(){};]', TokenType.BRACKETS),                      # Brackets and semicolons
      ]

      i = 0
      while i < len(text):
          matched = False
          for pattern, token_type in token_patterns:
              match = re.match(pattern, text[i:])
              if match:
                  token_value = match.group(0)
                  tokenlist.append(Token(token_value, token_type))
                  i += len(token_value)  # Move the index forward by the length of the match
                  matched = True
                  break
          if not matched:
              # If no match found, increment index by 1 to avoid infinite loop
              i += 1

      return tokenlist