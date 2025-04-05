from Token import *
from TokenType import *
import re

class Tokeniser:
  def __init__(self, tokenMap: dict[str, TokenType]):
      self.tokenMap = tokenMap

  def tokenize(self, text: str):
      tokenlist = []

      i = 0
      while i < len(text):
          # Skip whitespace
          if text[i].isspace():
              i += 1
              continue
              
          # Try regex patterns first
          token_patterns = [
              (r'(!=|<=|>=|&&|==|\|\|)', TokenType.LOGICAL_OPERATION),  
              (r'[\+\-\*/=]', TokenType.ARITHMETIC_OPERATION),       
              (r'[0-9]+\.[0-9]+', TokenType.VALUE),                  
              (r'"[^"]*"', TokenType.VALUE),                         
              (r'[0-9]+', TokenType.VALUE),                          
              (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.VARIABLE),       
              (r'[(){};]', TokenType.BRACKETS),                     
          ]

          matched = False
          for pattern, token_type in token_patterns:
              match = re.match(pattern, text[i:])
              if match:
                  token_value = match.group(0)
                  
                  # For variables, check if the entire token matches a keyword
                  # This prevents partial matches like seeing "if" in "ifElse"
                  if token_type == TokenType.VARIABLE and token_value in self.tokenMap:
                      token_type = self.tokenMap[token_value]
                  
                  # For other token types, also check if they're in tokenMap
                  elif token_value in self.tokenMap:
                      token_type = self.tokenMap[token_value]
                      
                  tokenlist.append(Token(token_value, token_type))
                  i += len(token_value)
                  matched = True
                  break
                  
          if not matched:
              # If no match found, increment index by 1 to avoid infinite loop
              i += 1

      return tokenlist