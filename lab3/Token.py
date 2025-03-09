import TokenType

class Token:
  def __init__(self, value, tokenType: TokenType):
    self.value = value
    self.tokenType = tokenType

  def __str__(self):
    return f"Token Value: {self.value} \t Token Type: {str(self.tokenType.name)}"    