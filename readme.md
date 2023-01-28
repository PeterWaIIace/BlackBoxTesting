# BlackBoxTesting - Zero Code generative testing framework

<img src="https://user-images.githubusercontent.com/40773550/215234611-2b3c1934-5ab4-4048-8442-89aabe0c0117.png#gh-light-mode-only" width="300" height="300">
<img src="https://user-images.githubusercontent.com/40773550/215234901-613934bb-5af3-40ab-8c26-7f1f5b88d123.png#gh-dark-mode-only" width="300" height="300">


This is experimental framework [WIP] for generating tests on the fly. The main purpose is to use it together with code generation models, allowing to self check of generated code (by ChatGPT/GPT3 or BLOOM).
## No dependencies

## Installation

[WIP]

## Example of usage:

[WIP]

1) Run in code test based on passed parameters (functionName, functionBody, Inputs, ExpOutputs)

```

from BlackBoxManager import BBTest

bbTest.generateTest("hello_world","def hello_world():\n   return \"hello world\"",[],["hello world"]);
report = bbTest.runTest()

```

2) Scan source code file and run test based on parameters in json (functionName, Inputs, ExpOutputs):

```

from BlackBoxManager import BBTest

bbTest = BBTest()
bbTest.scanAndGenerateTest('tests/test_file_python.py','tests/testing_file_for_file_scanner.json','funcName')
report = bbTest.runTest()

```
