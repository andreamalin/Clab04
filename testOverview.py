import pandas as pd
from test import batTesting
from Clab03 import clab03

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
        
clab = clab03()
print(testOverview().runTest(clab.b1))