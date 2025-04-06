#Variant 4 Vladimir Vitcovschii

class RegexMachine:
    MAX_REPEAT = 5  # Used for '*' and '+'

    def __init__(self, pattern):
        self.pattern = pattern

    def find_matching(self, start, open_char, close_char):
        depth = 0
        for i in range(start, len(self.pattern)):
            if self.pattern[i] == open_char:
                depth += 1
            elif self.pattern[i] == close_char:
                depth -= 1
                if depth == 0:
                    return i
        raise ValueError(f"Unmatched {open_char}")

    def parse_pattern(self):
        parts = []
        i = 0

        while i < len(self.pattern):
            char = self.pattern[i]

            # GROUP: (A|B)
            if char == '(':
                end = self.find_matching(i, '(', ')')
                group = self.pattern[i + 1:end].split('|')
                parts.append(group)
                i = end + 1

            # REPEAT: {3}
            elif char == '{':
                end = self.find_matching(i, '{', '}')
                repeat = int(self.pattern[i + 1:end])
                if not parts:
                    raise ValueError("Nothing to repeat before '{...}'")
                last = parts.pop()
                parts.append([''.join([item * repeat]) for item in last])
                i = end + 1

            # QUANTIFIERS: ?, *, +
            elif i + 1 < len(self.pattern) and self.pattern[i + 1] in '?*+':
                symbol = self.pattern[i + 1]
                base = self.pattern[i]

                if symbol == '?':
                    parts.append([base, ''])
                elif symbol == '*':
                    parts.append([base * j for j in range(0, self.MAX_REPEAT + 1)])
                elif symbol == '+':
                    parts.append([base * j for j in range(1, self.MAX_REPEAT + 1)])

                i += 2

            # MULTI-DIGIT LITERAL: '24'
            elif char.isdigit():
                start = i
                while i < len(self.pattern) and self.pattern[i].isdigit():
                    i += 1
                parts.append([self.pattern[start:i]])

            # DEFAULT: single character literal
            else:
                parts.append([char])
                i += 1
            #(X|Y|Z){2} is considered to be a double selection of the same object like xx yy zz and not their mix xy yx zy yz xz zx
            #But will be implemented in the next hour

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
        print(f"Generated strings for pattern: {self.pattern}")
        parts = self.parse_pattern()
        for string in self.generate_results(parts):
            print(string)
        print()

patterns = [
    '(S|T)(U|V)W*Y+24', 
    'L(M|N)D{3}P*Q(2|3)',
    'R*S(T|U|V)W(X|Y|Z){2}',
]
machines = [ RegexMachine(pattern) for pattern in patterns ]
[ machine.process() for machine in machines ]