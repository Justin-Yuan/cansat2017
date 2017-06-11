import csv

with open('cansat_2017.csv') as f:
    reader = csv.reader(f)
    # data = list(reader)
    for i in range(9):
        print(i)
        print(type(reader.next()))
