import itertools


class RegexMachine:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse_pattern(self):
        parts = []
        i = 0
        while i < len(self.pattern):
            if self.pattern[i] == '(':
                end = self.pattern.find(')', i)
                if end == -1:
                    raise ValueError("Unmatched parenthesis")
                group = self.pattern[i + 1:end].split('|')
                parts.append(group)
                i = end + 1
            elif self.pattern[i] == '{':
                end = self.pattern.find('}', i)
                if end == -1:
                    raise ValueError("Unmatched curly brace")
                repeat = int(self.pattern[i + 1:end])
                if parts:
                    last_part = parts.pop()
                    parts.append([''.join([c] * repeat) for c in last_part])
                i = end + 1
            elif i + 1 < len(self.pattern) and self.pattern[i + 1] in '?*+':
                if self.pattern[i + 1] == '?':
                    parts.append([self.pattern[i], ''])
                elif self.pattern[i + 1] == '*':
                    parts.append([*[ self.pattern[i] * j for j in range(0,6) ]])
                elif self.pattern[i + 1] == '+':
                    parts.append([*[ self.pattern[i] * j for j in range(1,6) ]])
                i += 2
            else:
                parts.append([self.pattern[i]])
                i += 1
        return parts

    @staticmethod
    def product(parts):
        if not parts:
            return []

        result = ['']
        for part in parts:
            temp = []
            for prefix in result:
                for item in part:
                    temp.append(prefix + item)
            result = temp
        return result

    def generate_results(self, parts):
        for combination in self.product(parts):
            yield ''.join(combination)

    def process(self):
        parts = self.parse_pattern()
        print("Generated strings:")
        for string in self.generate_results(parts):
            print(string)


patterns = [
    '(S|T)(U|V)W*Y+24', 
    'L(M|N)D{3}P*Q(2|3)',
    'R*S(T|U|V)W(X|Y|Z){2}',
]
machines = [ RegexMachine(pattern) for pattern in patterns ]
[ machine.process() for machine in machines ]