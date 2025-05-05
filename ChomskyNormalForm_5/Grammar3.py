from lab2.Grammar2 import Grammar2

EPSILON = 'ε'

class Grammar3(Grammar2):
    def __init__(self, **args):
        super().__init__(**args)

    def isCnf(self):
        for nonTerminal in self.P:
            for production in self.P[nonTerminal]:
                if len(production) == 0 or len(production) > 2:
                    return False
                if len(production) == 1 and production not in self.Vt:
                    return False
                if len(production) == 2 and any(symbol in self.Vt for symbol in production):
                    return False
        return True

    def eliminateEpsilonProductions(self):
        nullable = set()

        for nonTerminal in self.Vn:
            for production in self.P[nonTerminal]:
                if production == EPSILON:
                    nullable.add(nonTerminal)

        changes = True
        while changes:
            changes = False
            for nonTerminal in self.Vn:
                if nonTerminal not in nullable:
                    for production in self.P[nonTerminal]:
                        if all(symbol in nullable for symbol in production):
                            nullable.add(nonTerminal)
                            changes = True
                            break

        newRules = {}
        for nonTerminal in self.P:
            newProds = []
            for production in self.P[nonTerminal]:
                if production != EPSILON:
                    newProds.extend(self._expandNullableProd(production, nullable))
            newRules[nonTerminal] = list(set(newProds))

        self.P = newRules

    def _expandNullableProd(self, production, nullable):
        expansions = ['']

        for symbol in production:
            newExpansions = []
            if symbol in nullable:
                for expansion in expansions:
                    newExpansions.append(expansion + symbol)
                    newExpansions.append(expansion)
            else:
                for expansion in expansions:
                    newExpansions.append(expansion + symbol)
            expansions = newExpansions

        return [expansion for expansion in expansions if expansion]

    def eliminateRenaming(self):
        changes = True
        while changes:
            changes = False
            for nonTerminal in self.Vn:
                unitProductions = [p for p in self.P[nonTerminal] if p in self.Vn]
                for unit in unitProductions:
                    newProductions = self.P[unit]
                    if newProductions:
                        self.P[nonTerminal].extend(newProductions)
                        self.P[nonTerminal].remove(unit)
                        self.P[nonTerminal] = list(set(self.P[nonTerminal]))
                        changes = True
                self.P[nonTerminal] = [
                    p for p in self.P[nonTerminal] if p not in self.Vn
                ]

    def eliminateInaccessibleSymbols(self):
        accessible = {self.S}
        changes = True
        oldRules = self.P.copy()

        while changes:
            changes = False
            for nonTerminal in accessible.copy():
                for production in self.P[nonTerminal]:
                    for symbol in production:
                        if symbol in self.Vn and symbol not in accessible:
                            accessible.add(symbol)
                            changes = True

        self.Vn = list(accessible)
        self.P = {nt: oldRules[nt] for nt in accessible}

    def eliminateNonProductiveSymbols(self):
        productive = {self.S}
        changes = True

        while changes:
            changes = False
            for nonTerminal in self.Vn:
                if nonTerminal not in productive:
                    for production in self.P[nonTerminal]:
                        if all(symbol in self.Vt or symbol in productive for symbol in production):
                            productive.add(nonTerminal)
                            changes = True
                            break

        self.Vn = list(productive)
        updatedRules = {}
        for nt in productive:
            productiveRules = []
            for production in self.P[nt]:
                if all(symbol in self.Vt or symbol in productive for symbol in production):
                    productiveRules.append(production)
            updatedRules[nt] = productiveRules

        self.P = updatedRules

    def _createNewNonTerminal(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for letter in alphabet:
            if letter not in self.Vn:
                self.Vn.append(letter)
                return letter

        for letter in alphabet:
            for num in range(50):
                newSymbol = f'{letter}{num}'
                if newSymbol not in self.Vn:
                    self.Vn.append(newSymbol)
                    return newSymbol

        raise ValueError("Exhausted all possible non-terminal symbols.")

    def toCnf(self, printSteps=True):
        if self.isCnf():
            return

        self.eliminateEpsilonProductions()
        if printSteps:
            print('1. After eliminating epsilon productions:')
            print(self)
            print()

        self.eliminateRenaming()
        if printSteps:
            print('2. After eliminating renaming productions:')
            print(self)
            print()

        self.eliminateInaccessibleSymbols()
        if printSteps:
            print('3. After eliminating inaccessible symbols:')
            print(self)
            print()

        self.eliminateNonProductiveSymbols()
        if printSteps:
            print('4. After eliminating non-productive symbols:')
            print(self)
            print()

        rhsToNonTerminal = {}
        oldNonTerminals = list(self.P)

        newRules = {}
        for nonTerminal in list(self.P):
            newRules[nonTerminal] = set()
            for production in self.P[nonTerminal]:
                while len(production) > 2:
                    firstTwoSymbols = production[:2]

                    if firstTwoSymbols in rhsToNonTerminal:
                        newNonTerminal = rhsToNonTerminal[firstTwoSymbols]
                    else:
                        newNonTerminal = self._createNewNonTerminal()
                        newRules[newNonTerminal] = {firstTwoSymbols}
                        rhsToNonTerminal[firstTwoSymbols] = newNonTerminal

                    production = newNonTerminal + production[2:]

                newRules[nonTerminal].add(production)

        for nonTerminal, productions in list(newRules.items()):
            tempProductions = productions.copy()
            for production in tempProductions:
                if len(production) == 2 and any(symbol in self.Vt for symbol in production):
                    newProduction = []
                    for symbol in production:
                        if symbol in self.Vt:
                            if symbol in rhsToNonTerminal:
                                newNonTerminal = rhsToNonTerminal[symbol]
                            else:
                                newNonTerminal = self._createNewNonTerminal()
                                newRules[newNonTerminal] = {symbol}
                                rhsToNonTerminal[symbol] = newNonTerminal
                            newProduction.append(newNonTerminal)
                        else:
                            newProduction.append(symbol)
                    productions.remove(production)
                    productions.add(''.join(newProduction))

        self.P = {nt: newRules[nt] for nt in oldNonTerminals +
                      list(set(newRules) - set(oldNonTerminals))}

        if printSteps:
            print('5. After converting to CNF:')
            print(self)