#! /usr/bin/env python
# Read list of patients, go through dataList and retain only necessary patients
# Works on Python 3 only, not Python 2
# Version 2014-08-21

##### Parameters you can have fun playing with
headersToCompare = ['VISCODE', 'EXAMDATE']

##### The code which you shall not touch without my permission (but feel free to gaze at its ingenuity)
import csv
subjectList = "subjectsList.csv"
dataList = "dataList.csv"
outputList = "outputList.csv"


### Functions
def csv_object(csvfile):
    try:
        check = csvfile.read(1024)
        dialect = csv.Sniffer().sniff(check, delimiters=',\t ;:.')
        csvfile.seek(0)  # Goes back to beginning
        reader = csv.reader(csvfile, dialect)
    except:
        csvfile.seek(0)  # Goes back to beginning
        reader = csv.reader(csvfile, delimiter=',')
    return reader


def find_column(header, header_string):
    for column in range(len(header)):  # For each column in the header
        if header_string in header[column].strip().lower():  # If the column's header is RID
            return column
    return False

def find_rid(header, fileName):
    column = find_column(header,'rid')
    if column is False:
        print("No header with rid in ", fileName, ". I will assume rid's are in the first column.")
        column = 0  # Assuming First Column
    return column

def bleach_rid(rid):
    rid = ''.join(i for i in rid if i.isdigit()).lstrip('0')
    return rid


def list_rid(csvfile):
    csv_list = []
    reader = csv_object(csvfile)
    for row in reader:
        csv_list.append(row)
    return csv_list

# Read rid's
with open(subjectList, 'U') as csvfile:
    data1 = list_rid(csvfile)
with open(dataList, 'U') as csvfile:
    data2 = list_rid(csvfile)

secretStash = ["Giraffes are flamboyant: that is why they never sleep.",
               "There is a legend of a man who knows how to sing.",
               "Once upon a time, there was light. If only that happened once.",
               "If only the hippocampus could fly, we would all by dead by now.",
               "A bug is very much like a human being: it doesn't know why it lives."]

# Write dataList rows to output
try:
    with open(outputList, 'w', newline='') as csvfile:
        outputFile = csv.writer(csvfile)

        # Determine column for rid and other comparisons
        data1_ridColumn = find_rid(data1[0],'subjectsList.csv')
        data2_ridColumn = find_rid(data2[0],'dataList.csv')
        data1Columns = data2Columns = []
        for column_header in headersToCompare:
            data1Columns.append(find_column(data1[0], column_header))
            data2Columns.append(find_column(data2[0], column_header))

        # Actually compare the two lists
        for data1_row in data1:  # For each desired subject
            if not data1_row:
                continue
            found = 0
            for data2_row in data2:  # For each row in dataList.csv
                if bleach_rid(data1_row[data1_ridColumn]) == bleach_rid(data2_row[data2_ridColumn]):
                    if not headersToCompare:
                        found = 1
                    else:
                        for i in range(0,len(data1Columns)):
                            if data1_row[data1Columns[i]].strip() == data1_row[data2Columns[i]].strip():
                                found = 1

                if found == 1:
                    outputFile.writerow(data1_row + data2_row)
                    break
            if not found:
                outputFile.writerow(data1_row)
except PermissionError:
    print('Close the outputList.csv. How do you expect me to work in these conditions geez?')