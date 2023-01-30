
import copy
import timeit

def testcopy():
    for i in range(5):
        #numbers = [x for x in range(9999)]
        new = copy.copy(numbers)
        del numbers
        del new


def testdeepcopy():
    for i in range(5):
        numbers = [x for x in range(9999)]
        new = copy.deepcopy(numbers)
        del numbers
        del new


def testlist():
    for i in range(5):
        numbers = [x for x in range(9999)]
        new = list(numbers)
        del numbers
        del new

if __name__ == "__main__":
    print("Copy:\t" + str(timeit.timeit(testcopy, number=100)))
    print("Deep Copy:\t" + str(timeit.timeit(testdeepcopy, number=100)))
    print("List:\t" + str(timeit.timeit(testlist, number=100)))