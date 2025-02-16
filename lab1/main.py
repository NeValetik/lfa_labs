from Grammar import *

grammar = Grammar(
  Vn = {"S", "D", "R"},
  Vt = {"a", "b", "c"},
  P = {
    "S" : ["aS", "cD"],
    "D" : ["bR"],
    "R" : ["aR", "b", "cS"]
  },
  S = "S",
)

print("List of randomly generated valid strings:") 
print(*[grammar.generateValidString()  for _ in range(5)]) 

print("Random String Test:")
testStrings = ["cbb", "bac", "ca", "cb", "aaaa", "aaaaaab"]
fa = grammar.toFiniteAutomata()
for string in testStrings:
  print(f"{string}:{fa.stringValidation(string)}")

while True:
  inp = input("Enter any other random string (or empty to end): ")
  if inp == "":
    break
  print(f"{inp}: {fa.stringValidation(inp)}\n")