#Vitcovschii Vladimir FAF-231
# Variant 32
# Q = {q0,q1,q2},
# ∑ = {a,b,c},
# F = {q2},
# δ(q0,a) = q0,
# δ(q0,a) = q1,
# δ(q1,c) = q0,
# δ(q1,b) = q1,
# δ(q1,a) = q2,
# δ(q2,a) = q2.

from lab2.FiniteAutomata2 import *

states = { "q0", "q1", "q2" }
alphabet = { "a", "b", "c" }
transitions = {
  ( "q0", "a" ): [ "q0", "q1" ],
  ( "q1", "c" ): [ "q0" ],
  ( "q1", "b" ): [ "q1" ],
  ( "q1", "a" ): [ "q2" ],
  ( "q2", "a" ): [ "q2" ],
}
startState = "q0"
finalStates = [ "q2" ]

fa = FiniteAutomata2(
  states = states,
  alphabet = alphabet,
  transitions = transitions,
  startState = startState,
  finalStates = finalStates
)

gramma = fa.finiteAutomatonToGrammar()
print(gramma)
print(gramma.chomskyTypization())

print(fa.isDetermenistic())

dfa = fa.NfaToDfa()
print(dfa.isDetermenistic())



