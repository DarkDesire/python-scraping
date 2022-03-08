import csv

header = ['int', 'int plus 2', 'int plus 3']
datarow = lambda i: (i,i+2,i+3)

with open('test.csv', 'w+') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', lineterminator='\n')
    writer.writerow(header)
    for i in range(10):
        writer.writerow(datarow(i))