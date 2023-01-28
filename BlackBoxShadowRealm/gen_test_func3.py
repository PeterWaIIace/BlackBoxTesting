import sys

def func3(x,y):
    x = 3
    y = x + y
    return x + y


test_inputs  = [[1, 1], [2, 2], [3, 3]]
test_outputs = [2, 4, 6]

if __name__=="__main__":

    passed_tests = []

    output=func3(test_inputs[0][0],test_inputs[0][1])
    passed_tests.append(output == test_outputs[0])
    output=func3(test_inputs[1][0],test_inputs[1][1])
    passed_tests.append(output == test_outputs[1])
    output=func3(test_inputs[2][0],test_inputs[2][1])
    passed_tests.append(output == test_outputs[2])
    

    sys.stdout.buffer.write(bytes(passed_tests))