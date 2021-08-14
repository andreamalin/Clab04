import pandas as pd
from test import batTesting
from Clab03 import clab03

clab = clab03()

class testOverview():

    def __init__(self):
        self.bt = batTesting()
        self.df = pd.DataFrame(columns=['TEST','P-value','Conclusion'])
        
    def runTest(self, bitChain):
        bt = self.bt
        tests = [
            bt.test01(bitChain), bt.test02(bitChain), bt.test03(bitChain),
            bt.test04(bitChain), bt.test05(bitChain), bt.test06(bitChain),
            bt.test07(bitChain), bt.test08(bitChain), bt.test09(bitChain),
            bt.test10(bitChain)
        ]

        self.df['TEST'] = [
            'Monobit test', 'Random Excursion Variant test', 'DFT test',
            'Random Excursion test', 'Runs test', 'Longest Run Ones iab test',
            'Non Overlapping TM test', 'Cumulative Sums test', 'Approximate Entropy test',
            'test 10'
        ]
        for i in range(len(tests)):
            self.df['P-value'].iloc[i] = tests[i][0]
            self.df['Conclusion'].iloc[i] = tests[i][1]
           
        return self.df


    #def dataFrame(self):
        
print("---------------------------------------")
print("Cadenas de Buen Ocultamiento de Patrón")
print("---------------------------------------")
print("\nWichman-Hill de longitud 128,992\n")
print(testOverview().runTest(clab.b1))
print("\nLFSR con seed 11001001\n")
print(testOverview().runTest(clab.b2))
print("\nLCG (a:612 b:5,115 N:7,212)\n")
print(testOverview().runTest(clab.b3))
print("\n---------------------------------------")
print("Cadenas de Mal Ocultamiento de Patrón")
print("---------------------------------------\n")
print("\n LCG (a:6  b:55 N: 11)\n")
print(testOverview().runTest(clab.m1))
print("\nLCG (a:6  b:55 N: 37)\n")
print(testOverview().runTest(clab.m2))
print("\nLCG (a:6  b:55 N: 150)\n")
print(testOverview().runTest(clab.m3))