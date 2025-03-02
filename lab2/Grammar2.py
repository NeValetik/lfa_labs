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

import random
import lab1.FiniteAutomaton as fa
import lab1.Grammar as gram1


class Grammar(gram1):
  def chomskyTipisation(self):
    isType1 = True 
    isType2 = True  
    isType3Left = True 
    isType3Right = True  
    
    hasEmptyProduction = False
    for lhs, rules in self.P.items():
      for rule in rules:
        if rule == "": 
          if lhs != self.startSymbol or hasEmptyProduction:
            isType1 = False 
          hasEmptyProduction = True
    
    for lhs, rules in self.P.items():
      if len(lhs) != 1 or lhs not in self.vn:
        isType2 = isType3Right = isType3Left = False
        
      for rule in rules:
        if rule == "":
          isType3Right = isType3Left = False
          continue
      
        if any(c in self.vn for c in rule[:-1]):
          isType3Right = False

        if len(rule) > 1 and (rule[0] not in self.vn or any(c in self.vn for c in rule[1:])):
          isType3Left = False
    
        if len(rule) < len(lhs) and not (lhs == self.startSymbol and rule == ""):
          isType1 = False

    if isType3Right or isType3Left:
      return "Type 3: Regular Grammar"
    if isType2:
      return "Type 2: Context-Free Grammar"
    if isType1:
      return "Type 1: Context-Sensitive Grammar"
    return "Type 0: Unrestricted Grammar"
  

