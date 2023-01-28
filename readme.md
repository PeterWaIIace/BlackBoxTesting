# BlackBoxTesting - Zero Code generative testing framework

<img src="https://user-images.githubusercontent.com/40773550/215234611-2b3c1934-5ab4-4048-8442-89aabe0c0117.png#gh-light-mode-only" width="300" height="300">
<img src="https://user-images.githubusercontent.com/40773550/215234901-613934bb-5af3-40ab-8c26-7f1f5b88d123.png#gh-dark-mode-only" width="300" height="300">

### [WIP]

This is experimental framework for generating tests on the fly. The main purpose is to use it together with code generation models, allowing to self check of generated code (by ChatGPT/GPT3 or BLOOM).
## Features

- Scan file for functions to test
- Specify tests without writing test code
- Test Python (for now) functions [In future python classes as well as other languages probably]
- Simple to use
- Lightweight
- Code embeddable

## Dependencies

- no dependencies
## Installation

```
pip install git+https://github.com/PeterWaIIace/BlackBoxTesting
```

## Examples of usage:

#### Run tests based on target file and tests definition JSON:

Example of JSON defining tests:
```

{
    "func1":{"inputs": [[1,1],[2,2],[3,3]], "outputs": [5,8,11]},
    "func3":{"inputs": [[1,1],[4,2],[4,3]], "outputs": [9,16,17]}
}

```
Example of code:
```
bbTest = BBTest()
report = bbTest.generateTests('tests/test_file_python.py','tests/testing_file_for_file_scanner.json')

```

####  Run in code test based on passed parameters (functionName, functionBody, Inputs, ExpOutputs)

```

from BlackBoxManager import BBTest

bbTest.generateTest("hello_world","def hello_world():\n   return \"hello world\"",[],["hello world"]);
report = bbTest.runTest()

```

####  Scan source code file and run test based on parameters in json (functionName, Inputs, ExpOutputs):

```

from BlackBoxManager import BBTest

bbTest = BBTest()
bbTest.scanAndGenerateTest('tests/test_file_python.py','tests/testing_file_for_file_scanner.json','funcName')
report = bbTest.runTest()

```

## QuickStart:

1. Checkout repository
2. Execute `run_test.py`
3. Edit code in `run_test.py` or `tests/test_file_python.py`
4. Specify test definitions in `tests/testing_file_for_file_scanner.json`

