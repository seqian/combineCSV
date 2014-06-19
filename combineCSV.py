#! /usr/bin/env python
# Read list of patients, go through dataList and retain only necessary patients
# Works on Python 3 only, not Python 2
# Version 2014-06-18

##### Parameters you can have fun playing with
subjectList = "subjectsList.csv" # Will retrieve the list of rid's from this csv file.
dataList = "dataList.csv" # Will find the rows corresponding to the list of rid's from the subjectsList file.
outputList = "outputList.csv" # Will write the rows to this file.
keepAll = False # True or False. Will keep all the rows in dataList that correspond to a rid from subjectList. Note that if True you will have to manually choose which row you want to keep and delete.
skipLineIfNotFound = True # True or False. If True, will skip lines in outputList to align the rids with the subjectList.
headerString = 'rid' # Here, you can define the header of the column you want to use to match the two lists

##### The code which you shall not touch without my permission (but feel free to gaze at its ingenuity)
import csv, random

### Functions
def csvObject(csvfile):
    try:
        check = csvfile.read(1024)
        dialect = csv.Sniffer().sniff(check)
        csvfile.seek(0) # Goes back to beginning
        reader = csv.reader(csvfile, dialect)
    except:
        reader = csv.reader(csvfile, delimiter=',')
    return reader

def findRIDcolumn(header, fileName):
    whereIsRID = 0 # First Column by Default
    found = False
    for i in range(len(header)): #For each column in the header
        if headerString in header[i].strip().lower(): # If the column's header is RID
            whereIsRID = i
            found = True
            break
    if not found:
        print("No header with ", headerString, " in ", fileName,". I will assume rid's are in the first column.")
        whereIsRID = 0 # First Column by Default
    return whereIsRID

def bleachRID(rid):
    #newRid = rid.strip().lstrip('0')
    newRid = ''.join(i for i in rid if i.isdigit()).lstrip('0')
    return newRid

def listRID(csvfile):
    list = []
    reader = csvObject(csvfile)
    for row in reader:
        list.append(row)
    return list

# Read rid's
with open(subjectList, newline='') as csvfile:
    data1 = listRID(csvfile)
with open(dataList, newline='') as csvfile:
    data2 = listRID(csvfile)

secretStash = ["Giraffes are flamboyant: that is why they never sleep.","There is a legend of a man who knows how to sing.","Once upon a time, there was light. If only that happened once.","If only the hippocampus could fly, we would all by dead by now.","A bug is very much like a human being: it doesn't know why it lives."]

# Write dataList rows to output
try:
    with open(outputList, 'w', newline='') as csvfile:
        outputFile = csv.writer(csvfile)

        '''
        # Write down headers
        if header_data1:
            header1 = data1[0]
            ridColumn_data1 = findRIDcolumn(data1[0])
        else:
            header1 = []
        if header_data2:
            header2 = data2[0]
            ridColumn_data2 = findRIDcolumn(data2[0])
        else:
            header2 = []
        outputFile.writerow(header1 + header2)
        '''

        # Determine column for rid
        ridColumn_data1 = findRIDcolumn(data1[0],'subjectsList.csv')
        ridColumn_data2 = findRIDcolumn(data2[0],'dataList.csv')

        # Actually compare the two lists
        for rowling in data1: # For each desired subject
            if not rowling:
                continue
            found = 0
            for row in data2:
                if bleachRID(rowling[ridColumn_data1]) == bleachRID(row[ridColumn_data2]):
                    found = 1
                    outputFile.writerow(rowling + row)
                    if not keepAll:
                        break # Prevent duplicates
            if skipLineIfNotFound and not found:
                outputFile.writerow(rowling)
except PermissionError:
    print('Close the outputList.csv. How do you expect me to work in these conditions geez?')