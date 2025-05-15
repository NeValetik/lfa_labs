from lab3.TokenType import *
from lab3.Tokeniser import *
from parser6.Parser import *
from graphviz import Digraph

tokenMap = {
  "begin": TokenType.BEGIN,
  "end": TokenType.END,
  "if": TokenType.IF, 
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
tokens = tokeniser.tokenize("""
  begin
    if (x == 1) {
      print(10);
      y = 5;
    }
    print(100);
  end
""")

# Print just the token types for comparison with expected output
output = " ".join(token.tokenType.name for token in tokens)
print(output)

parser = Parser()
ast = parser.parse(tokens)
print("AST: ")
print(ast)

def visualize_ast(node, graph=None):
    if graph is None:
        graph = Digraph(format="png")
        graph.attr(rankdir="TB")

    node_label = f"{node.type}\n{node.value or ''}"
    graph.node(str(id(node)), label=node_label, shape="ellipse", style="filled", fillcolor="lightblue")

    for child in node.children:
        graph.edge(str(id(node)), str(id(child)))
        visualize_ast(child, graph)

    return graph


graph = visualize_ast(ast)
graph.render('ast', view=True)