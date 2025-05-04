# from constants import EPSILON
from ChomskyNormalForm_5.Grammar3 import Grammar3
from ChomskyNormalForm_5.Grammar3 import EPSILON 

nonTerminals = ['S', 'A', 'B', 'C']
terminals = ['a', 'b']
rules = {
    'S': ['abAB'],
    'A': ['aBSBab', 'BS', 'aA', 'b'],
    'B': ['BA', 'aBaBb', 'b', EPSILON],
    'C': ['AS'],
}

grammar = Grammar3(
  Vn = nonTerminals, Vt =  terminals, P = rules, S = "S"
)

print(grammar)

print("\n\nCNF:")
grammar.toCnf()