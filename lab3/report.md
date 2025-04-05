# Lexer & Scanner

**Course**: Formal Languages & Finite Automata\
**Author**: Vitcovschii Vladimir

---

## Theory

A **Lexer**, or lexical analyzer, is the first stage in the compilation or interpretation process. Its primary role is to read the input source code and convert it into a sequence of **tokens**, which are structured representations of syntactic elements such as keywords, operators, variables, values, and punctuation.

This lexer implementation in Python uses `Enum` classes to define and categorize token types for clarity and modularity.

### Token Types

Tokens are categorized using the following enums:

- **TokenType**: Main classification (e.g., `VALUE`, `VARIABLE`, `FUNCTION`)
- **ArithmeticOperation**: Includes `PLUS`, `MINUS`, `ASSIGN`, etc.
- **LogicalOperation**: Includes `AND`, `OR`, `EQUALS`, `MORE`, `LESS`, etc.
- **BuiltInFunction**: Includes `PRINT`, `SIN`, `COS`

This design allows extensibility and simplifies the process of mapping raw tokens to their semantic categories.

---

## Implementation Details

### Token Class

Each token is an object containing its value and type:

```python
class Token:
    def __init__(self, value, tokenType: TokenType):
        self.value = value
        self.tokenType = tokenType
```

### Tokeniser Class

The `Tokeniser` class is responsible for reading the input string and converting it into a list of tokens.

```python
class Tokeniser:
    def __init__(self, tokenMap: dict[str, TokenType]):
        self.tokenMap = tokenMap
```

The `tokenize()` method uses regex to match logical and arithmetic operators, literals (integers, floats, strings), variables, brackets, and keywords.

### Regex Patterns

Token patterns include:

- Logical: `!=`, `<=`, `>=`, `&&`, `==`, `||`
- Arithmetic: `+`, `-`, `*`, `/`, `=`
- Values: integers (`[0-9]+`), floats (`[0-9]+\.[0-9]+`), strings (`"[^"]*"`)
- Identifiers/variables: `[a-zA-Z_][a-zA-Z0-9_]*`
- Brackets and punctuation: `(){}[];`

---

## Error Handling

Currently, unrecognized characters are silently skipped (`i += 1`). This is acceptable for an early prototype, but improvements may include:

- Raising exceptions for invalid tokens
- Providing warnings with line/column info
- Logging tokenization issues for debugging

---

## Example Usage

```python
tokens = tokeniser.tokenize("begin if (+ 10 == 11); ifElse/11 != print(anton) sin cos end")
```

### Token Types Output

```
BEGIN IF BRACKETS ARITHMETIC_OPERATION VALUE LOGICAL_OPERATION VALUE BRACKETS END_LINE VARIABLE ARITHMETIC_OPERATION VALUE LOGICAL_OPERATION BUILT_IN_FUNCTIONS BRACKETS VARIABLE BRACKETS BUILT_IN_FUNCTIONS BUILT_IN_FUNCTIONS END
```

### Detailed Token List

```
begin: BEGIN  
if: IF  
(: BRACKETS  
+: ARITHMETIC_OPERATION  
10: VALUE  
==: LOGICAL_OPERATION  
11: VALUE  
): BRACKETS  
;: END_LINE  
ifElse: VARIABLE  
/: ARITHMETIC_OPERATION  
11: VALUE  
!=: LOGICAL_OPERATION  
print: BUILT_IN_FUNCTIONS  
(: BRACKETS  
anton: VARIABLE  
): BRACKETS  
sin: BUILT_IN_FUNCTIONS  
cos: BUILT_IN_FUNCTIONS  
end: END  
```

---

## Conclusion

This lexer implementation:

- Uses enums to classify and organize token types clearly.
- Employs regex patterns for accurate token recognition.
- Supports built-in functions, control flow keywords, variables, literals, and operators.
- Prepares tokens for downstream processing like parsing or interpretation.

### Potential Improvements

- Add line/column tracking for better error messages.
- Support context-sensitive analysis.
- Integrate with a parser for full language interpretation.

This project provides a foundational understanding of lexical analysis and the building blocks needed for compiler and interpreter development.

