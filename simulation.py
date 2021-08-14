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

    for _ in range(350):
      testResult = testRunner.runTest(prgs.wichmanhill(10000))
      failedTests = 10 - sum(list(testResult['Conclusion']))

      tests[failedTests] += 1

    for _ in range(350):
      testResult = testRunner.runTest(
          prgs.lfsr(10000, '11001001', (8, 7, 6, 1)))
      failedTests = 10 - sum(list(testResult['Conclusion']))

      tests[failedTests] += 1

    for _ in range(350):
      testResult = testRunner.runTest(
          prgs.LCG(612, 5115, 7212))
      failedTests = 10 - sum(list(testResult['Conclusion']))

      tests[failedTests] += 1

    showHistogram(tests)


if __name__ == '__main__':
    main()
