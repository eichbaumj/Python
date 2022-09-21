import database

#expression = b'[\x01-\xFF]\x00\x01{5}\x05\x01[\x00\x01][\x01-\x07]{2}\x25\x0F'
#db = 'talk.sqlite'
expression = b'[\x01-\xFF]\x00[\x01-\xFF]\x04[\x01-\xFF][\x01-\xFF]?[\x08\x09]\x08\x00[\x09\x01]\x08\x08\x01\x08\x00'
db = 'sms.db-wal'

offsets = database.getRecordOffsets(db, expression)
headers = database.getRecordHeaders(offsets)
records = database.parseRecords(headers)
for record in records:
    print(record)
