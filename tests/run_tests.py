from BlackBoxManager import BBTest, FileScanner

if __name__=="__main__":
    bbTest = BBTest(envFileName="gen_test_hello_world.py")
    bbTest.generateTest("hello_world","def hello_world():\n   return \"hello world\"",[],["hello world"]);
    print(bbTest.runTest())

    bbTest = BBTest(envFileName="gen_test_mul.py")
    bbTest.generateTest("mul","def mul(x,y):\n   return x*y",[[1,1],[2,2],[3,3]],[1,4,9])
    print(bbTest.runTest())

    fscan = FileScanner()

    funcName = 'func1'
    bbTest = BBTest(envFileName=f"gen_test_{funcName}.py")
    funcObj = fscan.scanFile('test_file_python.py',funcName)
    bbTest.generateTest(funcName,funcObj.code,[[1,1],[2,2],[3,3]],[2,4,6])
    print(bbTest.runTest())

    funcName = 'func3'
    bbTest = BBTest(envFileName=f"gen_test_{funcName}.py")
    funcObj = fscan.scanFile('test_file_python.py',funcName)
    bbTest.generateTest(funcName,funcObj.code,[[1,1],[2,2],[3,3]],[2,4,6])
    print(bbTest.runTest())
