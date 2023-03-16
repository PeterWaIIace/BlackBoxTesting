# WIP
import subprocess
import json
import os
import re

BB_ENV_NAME = "./BlackBoxShadowRealm/"
class BBManager:

    def __init__(self):

        self.resourceDir  = BB_ENV_NAME
        self.baseFileName = self.resourceDir+"environmentBase.py"
        self.baseFile = "import sys\n"+\
        "\n"+\
        "<TESTED_FUNCTION_BODY>\n"+\
        "\n"+\
        "test_inputs  = <TEST_INPUTS>\n"+\
        "test_outputs = <TEST_OUTPUTS>\n"+\
        "\n"+\
        "if __name__==\"__main__\":\n"+\
        "\n"+\
        "    passed_tests = []\n"+\
        "\n"+\
        "    <TESTED_FUNCTION_CALLS>\n"+\
        "\n"+\
        "    sys.stdout.buffer.write(bytes(passed_tests))"

        os.makedirs(os.path.dirname(self.baseFileName), exist_ok=True)
        with open(self.baseFileName,"w") as f:
            f.write(self.baseFile)

class BBTest:

    def __init__(self):
        self.ptrFuncBody       = "<TESTED_FUNCTION_BODY>"
        self.ptrFuncInvocation = "<TESTED_FUNCTION_CALLS>"
        self.ptrInputs         = "<TEST_INPUTS>"
        self.ptrOutputs        = "<TEST_OUTPUTS>"

        self.envFilePath = BB_ENV_NAME
        self.envFileName = "python_test_env.py"
        self.envBaseFileName = "environmentBase.py"

        self.fullPathToBase = self.envFilePath + "/" + self.envBaseFileName
        self.fullPathToTest = self.envFilePath + "/" + self.envFileName

    def __setEnvFilename(self,envFileName):
        self.envFileName = f"gen_test_{envFileName}.py"
        self.fullPathToTest = self.envFilePath + "/" + self.envFileName

    def __inputListToStr(self,inputs=[],n=0):
        allInputs = ""
        # get list of inputs
        if(hasattr(inputs[n], '__iter__')): # will fail for string what is good
            for i,_ in enumerate(inputs[n]):
                if i:
                    allInputs += f",test_inputs[{n}][{i}]"
                else:
                    allInputs += f"test_inputs[{n}][{i}]"
        else:
            allInputs += f"test_inputs[{n}]"

        return allInputs

    def scanAndGenerateTest(self,targetFileName,testsFileName,funcName):
        ## TO DO: write code which opens file and reads json and generate tests
        inputs  = []
        outputs = []
        with open(testsFileName, "r") as fTestDef:
            jTestDef = json.load(fTestDef)
            inputs = jTestDef[funcName]["inputs"]
            outputs = jTestDef[funcName]["outputs"]

        fScan  = FileScanner()
        funcObj = fScan.scanFile(targetFileName,funcName)

        self.__setEnvFilename(funcName)
        self.generateTest(funcName,funcObj.code,inputs,outputs)

        pass

    def generateTest(self,params={}):
        funcName=params["funcName"]
        funcBody=params["funcBody"]
        inputs = params["inputs"]
        outputs= params["outputs"]

        self.__setEnvFilename(funcName)

        self.inputs  = inputs
        self.outputs = outputs
        self.funcName = funcName

        fileContent = ""

        with open(self.fullPathToBase, "r") as f:
            fileContent = f.read()

        fileContent = fileContent.replace(self.ptrFuncBody,funcBody)

        for n,_ in enumerate(outputs):
            if len(inputs) > n:
                functionCall = f"output={funcName}({self.__inputListToStr(inputs,n)})\n"+\
                               f"    passed_tests.append(output == test_outputs[{n}])\n"+\
                               f"    {self.ptrFuncInvocation}"
                fileContent = fileContent.replace(self.ptrFuncInvocation,functionCall)

            else:
                functionCall = f"output={funcName}()\n"+\
                               f"    passed_tests.append(output == test_outputs[{n}])\n"+\
                               f"    {self.ptrFuncInvocation}"
                fileContent = fileContent.replace(self.ptrFuncInvocation,functionCall)

        fileContent = fileContent.replace(self.ptrFuncInvocation,"") # clean last call
        fileContent = fileContent.replace(self.ptrInputs,f"{inputs}")
        fileContent = fileContent.replace(self.ptrOutputs,f"{outputs}")

        with open(self.fullPathToTest, "w") as f:
            f.write(fileContent)


    def generateTest(self,funcName="",funcBody="",inputs=[],outputs=[]):
        self.inputs   = inputs
        self.outputs  = outputs
        self.funcName = funcName

        self.__setEnvFilename(funcName)

        fileContent = ""

        with open(self.fullPathToBase, "r") as f:
            fileContent = f.read()

        fileContent = fileContent.replace(self.ptrFuncBody,funcBody)

        for n,_ in enumerate(outputs):
            if len(inputs) > n:
                functionCall = f"output={funcName}({self.__inputListToStr(inputs,n)})\n"+\
                               f"    passed_tests.append(output == test_outputs[{n}])\n"+\
                               f"    {self.ptrFuncInvocation}"
                fileContent = fileContent.replace(self.ptrFuncInvocation,functionCall)

            else:
                functionCall = f"output={funcName}()\n"+\
                               f"    passed_tests.append(output == test_outputs[{n}])\n"+\
                               f"    {self.ptrFuncInvocation}"
                fileContent = fileContent.replace(self.ptrFuncInvocation,functionCall)

        fileContent = fileContent.replace(self.ptrFuncInvocation,"") # clean last call
        fileContent = fileContent.replace(self.ptrInputs,f"{inputs}")
        fileContent = fileContent.replace(self.ptrOutputs,f"{outputs}")

        with open(self.fullPathToTest, "w") as f:
            f.write(fileContent)

    def runTest(self):
        os.environ['PYTHONUNBUFFERED'] = '1'
        process = subprocess.Popen(f"python3 {self.fullPathToTest}", shell=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ) # Shell doesn't quite matter for this issue
        output = b''
        error = False

        while True:
            ret_err = process.stderr.readline()
            if(ret_err):
                error = True
                break

            tmp_output = process.stdout.readline()
            if tmp_output != b'':
                output = tmp_output

            if process.poll() is not None:
                break

        if error:
            return {},error

        rc = process.poll()
        results = list(output)

        report = {}
        for n,r in enumerate(results):
            if(n < len(self.inputs)):
                report[n] = {"funcName":self.funcName,"inputs":self.inputs[n],"outputs":self.outputs[n],"pass":results[n]}
            else:
                report[n] = {"funcName":self.funcName,"inputs":[],"outputs":self.outputs,"pass":results[n]}

        return {"report" : report, "system error" : error}

    def generateTests(self,targetCode="<SOURCE_CODE_TO_TEST>",filename="<JSON_FILE_WITH_TESTS_DEFS>"):

        functionsToTest = []
        with open(filename,"r") as f:
            fJson = json.load(f)
            functionsToTest = fJson.keys()

        reports = {}
        for funcName in functionsToTest:
            self.scanAndGenerateTest(targetCode,filename,funcName)
            reports[funcName] = self.runTest()

        return reports
class FunctionObject:

    def __init__(self,funcName,startLine):
        self.stopLine = 0
        self.startLine = startLine
        self.funcName = funcName
        self.code         = ''

    def setStartLine(self,startLine):
        self.startLine = startLine

    def startLine(self):
        return self.startLine

    def setStopLine(self,stopLine):
        self.stopLine = stopLine

    def appendLine(self,line):
        self.code += line

class FileScanner:

    def __init__(self):
        pass

    def findFunction(line):
        functionName = None

        if "def" in line:
            start = line.find("def ")
            end = line.find("(")
            functionName = line[start:end]

        return functionName

    def scanFunctions(self,fileName=None):
        funcObj = None
        line = "dummy"

        if not fileName:
            return None

        funcNames = []
        with open(fileName, 'r') as fileObject:
            while len(line) != 0:
                line = fileObject.readline()
                funcName = findFunction(line)
                if funcName:
                    funcNames.append(funcName)

        return funcNames

    def scanFile(self,fileName=None,funcName=None):
        funcObj = None

        if not fileName or not funcName:
            return None

        with open(fileName, 'r') as f:
            funcObj = self.functionExtractor(f,funcName)

        return funcObj

    def functionExtractor(self,fileObject,funcName):
        line = 'start' ## dummy word to start
        funcObj = None
        line_num = 0

        while len(line) != 0:
            line = fileObject.readline()
            rline = line.replace('\n','\\n')
            if funcName in line and "def" in line: ## Python dependent
                funcObj = FunctionObject(funcName,line_num)

            if funcObj:
                if funcObj.startLine != line_num and '\\n' == rline:
                    funcObj.setStopLine(line_num)
                    break

                else:
                    funcObj.appendLine(line)

            line_num += 1

        return funcObj


BBManager()

