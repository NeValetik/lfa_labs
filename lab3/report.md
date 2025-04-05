# Lexer & Scanner

**Course**: Formal Languages & Finite Automata\
**Author**: Vitcovschii Vladimir

---

## Theory

A **Lexer** (short for *lexical analyzer*) is a program or component responsible for breaking down a sequence of characters—usually source code—into a meaningful sequence of **tokens**. Tokens represent the smallest units of meaning, such as identifiers, literals, operators, delimiters, and keywords.

Lexical analysis is the **first step** in most compiler or interpreter pipelines. It translates raw source code into a stream of tokens which are then consumed by a parser.

This lexer implementation is written in Python, with token classification and structure heavily reliant on Python's `Enum` classes. This design ensures a high degree of modularity and extensibility.

### Why Enums?

The use of Python's `Enum` classes provides clarity, prevents errors due to typos, and makes the implementation easily expandable. Rather than comparing strings throughout the lexer, enums offer a well-defined set of expected categories.

### Token Categories

The lexer classifies tokens using several enums:

- **TokenType**: Describes broad categories of tokens such as `VALUE`, `VARIABLE`, `BUILT_IN_FUNCTIONS`, etc.
- **ArithmeticOperation**: Lists arithmetic operators like `+`, `-`, `*`, `/`, `=`.
- **LogicalOperation**: Covers logical operations such as `==`, `!=`, `&&`, `||`, etc.
- **BuiltInFunction**: Represents built-in functions that are reserved in the language like `print`, `sin`, `cos`.
- **ValueType**: (Used internally) Differentiates between `INT`, `FLOAT`, and `STRING` values.

---

## Implementation Details

The lexer operates in several clear stages:

### Token Class

The `Token` class encapsulates two main properties:

- `value`: the actual string content of the token (e.g., "10", "print", "+")
- `tokenType`: an instance of `TokenType`, providing a semantic label

```python
class Token:
    def __init__(self, value, tokenType: TokenType):
        self.value = value
        self.tokenType = tokenType

    def __str__(self):
        return f"Token Value: {self.value} \t Token Type: {str(self.tokenType.name)}"
```

### Tokeniser Class

The `Tokeniser` performs the core lexical analysis:

```python
class Tokeniser:
    def __init__(self, tokenMap: dict[str, TokenType]):
        self.tokenMap = tokenMap
```

#### `tokenize(text: str)` method

This method reads the input character by character and matches against regular expressions to identify known token types. The match order matters: complex tokens (like `!=`) are matched before simple ones (`=`).

The core loop:

- Skips whitespace
- Checks regex patterns in order
- Matches the longest valid token
- Falls back to unknown classification if no pattern matches

### Regex Matching Logic

```python
(r'(!=|<=|>=|&&|==|\|\|)', TokenType.LOGICAL_OPERATION),
(r'[\+\-\*/=]', TokenType.ARITHMETIC_OPERATION),
(r'[0-9]+\.[0-9]+', TokenType.VALUE),
(r'"[^"]*"', TokenType.VALUE),
(r'[0-9]+', TokenType.VALUE),
(r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.VARIABLE),
(r'[(){};]', TokenType.BRACKETS),
```

This pattern list allows accurate categorization and ordering of precedence for matching.

### Special Handling

If a `VARIABLE` matches a known keyword (e.g., `print`, `if`), it is upgraded to that specific `TokenType`. This is checked using `tokenMap`.

If a character sequence cannot be matched by any known pattern, it is classified as `UNKNOWN` and processed accordingly.

---

## Error Handling

The lexer gracefully handles unexpected or malformed input:

- Characters or sequences not matching any pattern are assigned the type `UNKNOWN`
- Multiple strategies for unknowns: checking non-alphanumeric symbols, prefix-based mismatches, or single characters
- Prevents crashing and provides full token coverage of input

---

## Example Usage

```python
code = "begin if (+ 10 == 11); ifElse/11 != print(anton) sin cos end"
tokens = tokeniser.tokenize(code)
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

This project demonstrates a clean and extensible implementation of a lexical analyzer in Python. It introduces the foundational concepts necessary for compiler or interpreter design.

### Highlights

- Modular structure with clear class responsibilities
- Enum usage for semantic clarity
- Regex-based token matching
- Supports keywords, built-in functions, operators, values, and brackets
- Handles malformed input gracefully

### Potential Improvements

- Add line/column tracking for better error messages
- Support for multiline string values and comments
- Integration with a full parser or interpreter
- Context-sensitive lexing (e.g., differentiate between `-` as negation vs subtraction)

This project offers a solid baseline for further language tool development, and introduces the student to the essential first phase of language processing: lexical analysis.

