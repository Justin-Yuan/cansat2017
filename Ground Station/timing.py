import timeit
import csv
filename = "abc.csv"
global csvwriter
def test():
    with open(filename, 'aw+') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=["0","2","3"])
        csvwriter.writerow({"0":1, "2":2, "3":3})
if __name__ == "__main__":
    print timeit.timeit("test()", setup = "from __main__ import test", number=100)
