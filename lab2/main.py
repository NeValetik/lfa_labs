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
from graphviz import Digraph

def visualize_fa(fa: FiniteAutomata2, title):
    graph = Digraph(comment=title)
    graph.attr(rankdir='LR')

    # Add states
    for state in fa.states:
        if state in fa.finalStates:
            graph.node(state, shape='doublecircle')
        else:
            graph.node(state, shape='circle')

    graph.node('start', shape='none', label='')
    graph.edge('start', fa.startState)

    for fromState, transitions in fa.transitions.items():
        for toStates in transitions:
            if isinstance(toStates, str):
                graph.edge(fromState[0], toStates, label=fromState[1])
            else:
                for toState in toStates:
                    graph.edge(fromState[0], toState, label=fromState[1])

    graph.render(f'{title}.gv', view=True)

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
print("The grammar from the given automation " + str(gramma))
# print(gramma.chomskyTypization())
print(fa)
print("Is the current fa determenistic? " + str(fa.isDetermenistic()))

dfa = fa.NfaToDfa()
print(dfa)
print("Is the fa determenistic now? " + str(dfa.isDetermenistic()))

visualize_fa(fa, 'NFA')
visualize_fa(dfa, 'DFA')


