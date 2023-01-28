from src.BlackBoxManager import BBTest

if __name__=="__main__":

    print("================================= START ====================================")
    print("================================= MANUALLY SPECIFIED ====================================")
    bbTest = BBTest()
    bbTest.generateTest("hello_world","def hello_world():\n   return \"hello world\"",[],["hello world"]);
    print(bbTest.runTest())

    bbTest = BBTest()
    bbTest.generateTest("mul","def mul(x,y):\n   return x*y",[[1,1],[2,2],[3,3]],[1,4,9])
    print(bbTest.runTest())

    print("================================= MANUALLY SPECIFIED AND SCANNED ====================================")

    funcName = 'func1'
    bbTest = BBTest()
    bbTest.scanAndGenerateTest('tests/test_file_python.py','tests/testing_file_for_file_scanner.json',funcName)
    print(bbTest.runTest())

    funcName = 'func3'
    bbTest = BBTest()
    bbTest.scanAndGenerateTest('tests/test_file_python.py','tests/testing_file_for_file_scanner.json',funcName)
    print(bbTest.runTest())

    print("================================= JSON SPECIFIED ====================================")

    bbTest = BBTest()
    report = bbTest.generateTests('tests/test_file_python.py','tests/testing_file_for_file_scanner.json')
    print(report)