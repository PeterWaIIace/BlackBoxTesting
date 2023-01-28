from src.BlackBoxManager import BBTest

if __name__=="__main__":
    bbTest = BBTest()
    bbTest.generateTest("hello_world","def hello_world():\n   return \"hello world\"",[],["hello world"]);
    print(bbTest.runTest())

    bbTest = BBTest()
    bbTest.generateTest("mul","def mul(x,y):\n   return x*y",[[1,1],[2,2],[3,3]],[1,4,9])
    print(bbTest.runTest())

    funcName = 'func1'
    bbTest = BBTest()
    bbTest.scanAndGenerateTest('tests/test_file_python.py','tests/testing_file_for_file_scanner.json',funcName)
    print(bbTest.runTest())

    funcName = 'func3'
    bbTest = BBTest()
    bbTest.scanAndGenerateTest('tests/test_file_python.py','tests/testing_file_for_file_scanner.json',funcName)
    print(bbTest.runTest())
