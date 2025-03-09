from Token import *
from TokenType import *
import re

class Tokeniser:
  def __init__(self, tokenMap: dict[str, TokenType]):
    self.tokenMap = tokenMap

  def tokenize(self, text: str):
    tempList = text.split()
    tokenlist = []

    for word in tempList:
      if word in self.tokenMap:
        tokenlist.append(Token(word, self.tokenMap[word]))
        continue

      lexema = ""
      i = 0
      while i < len(word):
        found = False

        for j in range(len(word), i, -1):
          substring = word[i:j]

          if substring in self.tokenMap:
            tokenlist.append(Token(substring, self.tokenMap[substring]))
            i = j - 1
            found = True
            break

        if not found:
          lexema += word[i]

        i += 1

      if lexema:
        # String value (enclosed in quotes)
        if lexema.startswith('"') and lexema.endswith('"'):
          tokenlist.append(Token(lexema, TokenType.VALUE))
        # Integer value (pure digits)
        elif re.match(r'^\d+$', lexema):
          tokenlist.append(Token(lexema, TokenType.VALUE))
        # Float value (contains a dot)
        elif re.match(r'^\d+\.\d+$', lexema):
          tokenlist.append(Token(lexema, TokenType.VALUE))
        else:
          # If it's not a value, treat it as a variable
          tokenlist.append(Token(lexema, TokenType.VARIABLE))  

    return tokenlist