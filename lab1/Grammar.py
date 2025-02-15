from FiniteAutomaton import * 
import random
class Grammar:

  def __init__(self, **args):
    self.Vn = args.get("Vn")
    self.Vt = args.get("Vt")
    self.P = args.get("P")
    self.S = args.get("S")

  def generate_valid_string(self):
    current = self.S        
    while any(symbol in self.Vn for symbol in current):
      new_string = ""
      for symbol in current:
        if symbol in self.Vn:
          new_string += random.choice(self.P[symbol])
        else:
          new_string += symbol
      current = new_string
    return current

  def to_finite_automata(self):
    states = set(self.Vn) | {""}
    alphabet = set(self.Vt)
    transitions = {}
    start_state = self.S
    final_states = {""}

    for non_terminal, rules in self.P.items():
      for rule in rules:
        if len(rule) == 1 and rule in self.Vt:
          if (non_terminal, rule) not in transitions:
            transitions[(non_terminal, rule)] = set()
          transitions[(non_terminal, rule)].add("")
        elif len(rule) >= 1:
          first_symbol = rule[0] 
          next_state = rule[1:] if len(rule) > 1 else ""
          
          if (non_terminal, first_symbol) not in transitions:
            transitions[(non_terminal, first_symbol)] = set()
          transitions[(non_terminal, first_symbol)].add(next_state)
    return FiniteAutomata(states, alphabet, transitions, start_state, final_states)      