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
print("Generate already valid strings:")
[print(grammar.generate_valid_string()) for _ in range(5)]

print("\nTesting random strings:")
test_strings = ["acab", "bac", "ca", "cb", "aaaa", "aaaaaab"]
fa = grammar.to_finite_automata()
for string in test_strings:
    print(f"{string}:{fa.string_validation(string)}")
while True:
    user_input = input("Enter any other random string (or empty to end): ")
    if user_input == "":
        print("Exiting")
        break
    print(f"{user_input}: {fa.string_validation(user_input)}\n")