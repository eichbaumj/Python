'''
This module contains functions made to parse through a database looking for a regular expression for record headers
getRecordOffsets: The first function to be called. Two arguments are needed; database and expression
The function will return a list of offsets found for the instances of the expression used

Example of database name and expression assignment:
expression = b'[\x01-\xFF]\x00\x01{5}\x05\x01[\x00\x01][\x01-\x07]{2}\x25\x0F'
db = 'talk.sqlite'

Example of getRecordOffsets function:
offsets = database.getRecordOffsets(db, expression)

getRecordHeaders: The second function to be called. This requires one argument, the offsets found above
This function will return a dictionary of headers based on the record size found at offset[0]

Example of getRecordHeaders function:
headers = database.getRecordHeaders(offsets)

parseRecords: The third function to be called. This requires one argument, the headers found above
This function will return a list of records after using the header to parse through the payload.

Example of parseRecords function:
records = database.parseRecords(headers)

parseVarInt: A function used while parsing the records but can also be used on its own to calculate a VarInt

Once the first three functions are called, a for loop can be used to iterate through the records list
for record in records:
    print(record)

This module most likely will not parse records found in freeblocks
This module should find records in freelist pages since those records will still have an intact header
This module is meant as a tool to assist in finding possible deleted records not displayed within a database viewer
This module is not meant as a complete tool to recover every record within a database
This module was written by James Eichbaum (eichbaumj@gmail.com) and the author assumes no responsibility for
the accuracy or completeness of the results from it
'''

import re
import struct

def getRowID(offset):
    i = 2
    if db[offset - i] > 127:
        i = 2
        while db[offset - i] > 127:
            i += 1
        varInt = db[offset - i + 1:offset]
        rowID = parseVarInt(varInt)
        return rowID
    else:
        rowID = db[offset -1]
        return rowID

def parseVarInt(hexinput):
    numofvalues = len(hexinput)
    this = 0
    last = (hexinput[numofvalues -1] <<1)
    count = 2
    leftshift = 8
    while (numofvalues - count) >= 0:
        this = ((((hexinput[numofvalues - count] << 1) & 0xFF) >> 1) << leftshift)
        last = (this | last)
        count += 1
        leftshift += 7
    return(last >> 1)

def getRecordOffsets(database,expression):
    global db
    offsets = []
    file = open('{}'.format(database), 'rb')
    db = file.read()
    file.close()
    for pattern in re.finditer(re.compile(expression), db):
        offset = pattern.start()
        offsets.append(offset)
    return offsets

def getSize(value):
    if value % 2:
        return ((value - 13) // 2, "String")
    else:
        return ((value - 12) // 2, "Blob")

def getRecordHeaders(offsets):
    headers = {}
    for offset in offsets:
        header = []
        rowID = getRowID(offset)
        if rowID:
            header_length = db[offset]
            header.append((offset, "Offset"))
            header.append((header_length, "Header"))
            header.append((rowID, "rowID"))
            pos = 2
            while pos < header_length:
                loc = offset + pos
                if db[loc] == 0:
                    header.append((0, "Null"))
                elif db[loc] < 5 and db[loc] > 0:
                    header.append((db[loc], "Integer"))
                elif db[loc] == 5:
                    header.append((6, 'Integer'))
                elif db[loc] == 6:
                    header.append((8, 'Integer'))
                elif db[loc] == 7:
                    header.append((8, 'Float'))
                elif db[loc] == 8:
                    header.append(('A', 0))
                elif db[loc] == 9:
                    header.append(('B', 1))
                else:
                    if db[loc] > 127:
                        value = (((db[loc]<<1) & 0xFF) << 6) | db[loc+1]
                        header.append(getSize(value))
                        pos += 1
                        pass
                    else:
                        header.append(getSize(db[loc]))
                pos += 1
            headers[rowID] = header
    return headers

def parseRecords(headers):
    records = []
    for header in headers:
        data = []
        offset = headers[header][0][0] + headers[header][1][0]
        data.append(headers[header][2][0])
        for data_item in headers[header][3:]:
            if data_item[1] == 'String':
                try:
                    data.append((db[offset:offset+data_item[0]]).decode('UTF-8'))
                except:
                    data.append((db[offset:offset+data_item[0]]))
                offset += data_item[0]
            elif data_item[1] == 'Blob':
                data.append('Blob')
                offset += data_item[0]
            elif data_item[1] == 'Integer':
                data.append(int.from_bytes(db[offset:offset + data_item[0]], 'big'))
                offset += data_item[0]
            elif data_item[1] == 'Null':
                data.append('Null')
            elif data_item[1] == 'Float':
                data.append(struct.unpack('>d', db[offset:offset + data_item[0]])[0])
                offset += data_item[0]
            elif data_item[1] == 0:
                data.append(0)
            elif data_item[1] == 1:
                data.append(1)
        records.append(data)
    return records
