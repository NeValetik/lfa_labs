import unittest

from ChomskyNormalForm_5.Grammar3 import Grammar3, EPSILON

class TestGrammar(unittest.TestCase):
    def setUp(self):
        # Variant 32 grammar
        nonTerminals = ['S', 'A', 'B', 'C']
        terminals = ['a', 'b']
        rules = {
            'S': ['abAB'],
            'A': ['aBSBab', 'BS', 'aA', 'b'],
            'B': ['BA', 'aBaBb', 'b', EPSILON],
            'C': ['AS'],
        }
        self.grammar = Grammar3(Vn = nonTerminals, Vt =  terminals, P = rules, S = "S")

    def testInitialGrammar(self):
        self.assertEqual(self.grammar.nonTerminals, ['S', 'A', 'B', 'C', 'D'])
        self.assertEqual(self.grammar.terminals, ['a', 'b'])
        self.assertIn('S', self.grammar.rules)
        self.assertIn('A', self.grammar.rules)
        self.assertIn('B', self.grammar.rules)
        self.assertIn('C', self.grammar.rules)
        self.assertIn('D', self.grammar.rules)

    def testEliminateEpsilonProductions(self):
        self.grammar.eliminateEpsilonProductions()
        self.assertNotIn(EPSILON, self.grammar.rules['D'])

    def testEliminateRenamingProductions(self):
        self.grammar.eliminateEpsilonProductions()
        self.grammar.eliminateRenaming()
        for prods in self.grammar.rules.values():
            for prod in prods:
                self.assertNotIn(prod, self.grammar.nonTerminals)

    def testEliminateInaccessibleSymbols(self):
        self.grammar.eliminateEpsilonProductions()
        self.grammar.eliminateRenaming()
        self.grammar.eliminateInaccessibleSymbols()
        for nt in self.grammar.nonTerminals:
            self.assertIn(nt, self.grammar.rules)

    def testEliminateNonProductiveSymbols(self):
        self.grammar.eliminateEpsilonProductions()
        self.grammar.eliminateRenaming()
        self.grammar.eliminateInaccessibleSymbols()
        self.grammar.eliminateNonProductiveSymbols()
        for prods in self.grammar.rules.values():
            for prod in prods:
                self.assertTrue(all(
                    symbol in self.grammar.terminals or symbol in self.grammar.nonTerminals for symbol in prod))

    def testIsCnf(self):
        self.assertFalse(self.grammar.isCnf())
        self.grammar.toCnf(printSteps=False)
        self.assertTrue(self.grammar.isCnf())

    def testToCnf(self):
        self.grammar.toCnf(printSteps=False)
        for nt, prods in self.grammar.rules.items():
            for prod in prods:
                self.assertTrue(len(prod) <= 2)
                if len(prod) == 2:
                    self.assertTrue(
                        all(symbol in self.grammar.nonTerminals for symbol in prod))
                if len(prod) == 1:
                    self.assertTrue(
                        prod in self.grammar.terminals or prod == EPSILON)


if __name__ == '__main__':
    unittest.main()