#! /usr/bin/env python
# Read list of patients, go through dataList and retain only necessary patients
# Works on Python 3 only, not Python 2
# Version 2014-08-21

##### Parameters you can have fun playing with
compareVisCode = True
keepAll = False

### Options Instructions
# subjectsList specifies the csv file with the list of subjects.
# dataList specifies the csv file with the data.
# outputList specifies the output csv file.
# compareVisCode. If enabled, it will only match rows with the same visit code. Especially useful with ADNI.
# keepAll determines whether to keep all the rows in dataList that correspond to a rid from subjectList. \
# Note that if True you will have to manually choose which row you want to keep and delete.
# skipLineIfNotFound determines whether to skip lines in outputList to align the rows with rids.


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
    column_number = 0  # First Column by Default
    found = False
    for i in range(len(header)):  # For each column in the header
        if header_string in header[i].strip().lower():  # If the column's header is RID
            column_number = i
            found = True
            break
    if not found:
        column_number = 0  # First Column by Default
    return column_number


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

        # Determine column for rid
        data1_ridColumn = find_column(data1[0], 'rid')
        data2_ridColumn = find_column(data2[0], 'rid')

        # Determine column for visitCode
        if compareVisCode:
            data1_visColumn = find_column(data1[0], 'VISCODE')
            data2_visColumn = find_column(data2[0], 'VISCODE')

        # Actually compare the two lists
        for rowling in data1:  # For each desired subject
            if not rowling:
                continue
            found = 0
            for row in data2:  # For each row in dataList.csv
                if bleach_rid(rowling[data1_ridColumn]) == bleach_rid(row[data2_ridColumn]):
                    if compareVisCode:
                        # noinspection PyUnboundLocalVariable
                        if rowling[data1_visColumn].strip() == rowling[data2_visColumn].strip():
                            found = 1
                    else:
                        found = 1
                if found == 1:
                    outputFile.writerow(rowling + row)
                    if not keepAll:
                        break  # Prevent duplicates
                if not found:
                  outputFile.writerow(rowling)
except PermissionError:
    print('Close the outputList.csv. How do you expect me to work in these conditions geez?')