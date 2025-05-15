from lab3.TokenType import TokenType

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        type_name = self.type.name if isinstance(self.type, TokenType) else self.type
        return f"{type_name}({self.value}, {self.children})"

'''
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
  BRACKETS = 11
  UNKNOWN = 12
  IF=13
'''

class Parser:
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0

        self.expect(TokenType.BEGIN)
        program_node = ASTNode(TokenType.BEGIN, value="program")

        while not self.check(TokenType.END):
            stmt = self.parse_statement()
            program_node.children.append(stmt)

        self.expect(TokenType.END)
        return program_node

    def parse_statement(self):
        if self.check(TokenType.IF):
            return self.parse_if()
        elif self.check(TokenType.BUILT_IN_FUNCTIONS):
            stmt = self.parse_function_call()
        elif self.check(TokenType.VARIABLE):
            stmt = self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

        self.expect(TokenType.END_LINE)
        return stmt

    def parse_if(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.BRACKETS, "(")
        condition = self.parse_expression()
        self.expect(TokenType.BRACKETS, ")")

        # Parse a block or a single statement
        if self.check(TokenType.BRACKETS, "{"):
            then_branch = self.parse_block()
        else:
            then_branch = self.parse_statement()

        return ASTNode("IF", [condition, then_branch])

    def parse_block(self):
        self.expect(TokenType.BRACKETS, "{")
        block_node = ASTNode("BLOCK")

        while not self.check(TokenType.BRACKETS, "}"):
            stmt = self.parse_statement()
            block_node.children.append(stmt)

        self.expect(TokenType.BRACKETS, "}")
        return block_node

    def parse_assignment(self):
        var = self.expect(TokenType.VARIABLE)
        self.expect(TokenType.ARITHMETIC_OPERATION, "=")
        expr = self.parse_expression()
        return ASTNode("ASSIGNMENT", [ASTNode(TokenType.VARIABLE, value=var.value), expr])

    def parse_function_call(self):
        func = self.expect(TokenType.BUILT_IN_FUNCTIONS)
        self.expect(TokenType.BRACKETS, "(")
        arg = self.parse_expression()
        self.expect(TokenType.BRACKETS, ")")
        return ASTNode("FUNC_CALL", [arg], value=func.value)

    def parse_expression(self):
        left = self.parse_term()
        while self.check(TokenType.ARITHMETIC_OPERATION) or self.check(TokenType.LOGICAL_OPERATION):
            op = self.advance()
            right = self.parse_term()
            left = ASTNode(op.tokenType, [left, right], value=op.value)
        return left

    def parse_term(self):
        if self.check(TokenType.VALUE) or self.check(TokenType.VARIABLE):
            return ASTNode(self.advance().tokenType, value=self.tokens[self.pos - 1].value)
        elif self.check(TokenType.BUILT_IN_FUNCTIONS):
            return self.parse_function_call()
        elif self.match(TokenType.BRACKETS, "("):
            expr = self.parse_expression()
            self.expect(TokenType.BRACKETS, ")")
            return expr
        else:
            raise SyntaxError(f"Unexpected term: {self.peek()}")

    # Helpers
    def check(self, token_type, value=None):
        if self.pos >= len(self.tokens):
            return False
        token = self.tokens[self.pos]
        if token.tokenType != token_type:
            return False
        if value is not None and token.value != value:
            return False
        return True

    def match(self, token_type, value=None):
        if self.check(token_type, value):
            self.advance()
            return True
        return False

    def expect(self, token_type, value=None):
        if not self.check(token_type, value):
            raise SyntaxError(f"Expected {token_type.name} {value}, got {self.peek()}")
        return self.advance()

    def advance(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
