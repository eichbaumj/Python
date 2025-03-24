#!/usr/bin/env python3
import sys
import sqlite3
import binascii

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} NoteStore.sqlite")
    sys.exit(1)

database = sys.argv[1]

try:
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = """
    SELECT Z_PK, ZCRYPTOITERATIONCOUNT, ZCRYPTOSALT, ZCRYPTOWRAPPEDKEY
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZISPASSWORDPROTECTED = 1
    """
    cursor.execute(query)

    with open("hashcat_input.txt", "w") as f:
        for row in cursor.fetchall():
            z_pk = row[0]
            iteration_count = row[1]
            salt = binascii.hexlify(row[2]).decode()
            wrapped_key = binascii.hexlify(row[3]).decode()
            line = f"$ASN$*{z_pk}*{iteration_count}*{salt}*{wrapped_key}\n"
            f.write(line)
            print(line.strip())

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    sys.exit(1)

finally:
    if conn:
        conn.close()
