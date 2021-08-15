import test
from testOverview import TestOverview
from Clab03 import clab03
from matplotlib import pyplot as plt


def showHistogram(tests):
    values = list(tests.values())
    xtitle = list(tests.keys())

    plt.bar(xtitle, values)
    plt.show()


def main():
    # Se obtienen las variables que se utilizaran
    tests = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    prgs = clab03()
    testRunner = TestOverview()
    n = 1000

    # for _ in range(n):
    #   testResult = testRunner.runTest(prgs.wichmanhill(10000))
    #   failedTests = 10 - sum(list(testResult['Conclusion']))

    #   tests[failedTests] += 1
    # showHistogram(tests)
    # print('primero')
    # for i in range(1, 11):
    #   print(i, tests[i]/n)
    # tests = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    # for _ in range(n):
    #   testResult = testRunner.runTest(
    #       prgs.lfsr(10000, '11001001', (8, 7, 6, 1)))
    #   failedTests = 10 - sum(list(testResult['Conclusion']))

    #   tests[failedTests] += 1
    # showHistogram(tests)
    # print('segundo')
    # for i in range(1, 11):
    #   print(tests[i]/n)
    # tests = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    for _ in range(n):
        testResult = testRunner.runTest(
            prgs.LCG(612, 5115, 7212))
        failedTests = 10 - sum(list(testResult['Conclusion']))

        tests[failedTests] += 1
    print('tercero')
    for i in range(1, 11):
        print(tests[i]/n)
    showHistogram(tests)


def main2():
    # Se obtienen las variables que se utilizaran
    tests = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    prgs = clab03()
    testRunner = TestOverview()

    for _ in range(350):
        testResult = testRunner.runTest(
            prgs.LCG(6, 55, 11))
        failedTests = 10 - sum(list(testResult['Conclusion']))

        tests[failedTests] += 1

    for _ in range(350):
        testResult = testRunner.runTest(
            prgs.LCG(6, 55, 37))
        failedTests = 10 - sum(list(testResult['Conclusion']))

        tests[failedTests] += 1

    for _ in range(350):
        testResult = testRunner.runTest(
            prgs.LCG(6, 55, 150))
        failedTests = 10 - sum(list(testResult['Conclusion']))

        tests[failedTests] += 1

    showHistogram(tests)


if __name__ == '__main__':
    main()
