#!/usr/bin/env python3

import sys
import sqlite3
import binascii
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <NoteStore.sqlite> <z_pk> <password>")
        sys.exit(1)

    db_path = sys.argv[1]
    z_pk = int(sys.argv[2])
    password = sys.argv[3]

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the locked note with the specified PK
    query = """
    SELECT ZCRYPTOITERATIONCOUNT, ZCRYPTOSALT
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZISPASSWORDPROTECTED = 1
      AND Z_PK = ?
    """
    cursor.execute(query, (z_pk,))
    row = cursor.fetchone()

    if not row:
        print(f"[!] No locked note found with PK={z_pk}.")
        conn.close()
        sys.exit(1)

    iteration_count, salt = row
    if salt is None or iteration_count is None:
        print(f"[!] Missing salt or iteration count for note PK={z_pk}.")
        conn.close()
        sys.exit(1)

    # Derive the 16-byte KEK using PBKDF2-HMAC-SHA256
    kek = PBKDF2(
        password,
        salt,
        dkLen=16,               # Apple uses 16-byte KEKs
        count=iteration_count,  # from ZCRYPTOITERATIONCOUNT
        hmac_hash_module=SHA256
    )

    # Convert to hex for easy display
    kek_hex = binascii.hexlify(kek).decode()

    print(f"Note PK={z_pk}: KEK (hex) = {kek_hex}")

    conn.close()

if __name__ == "__main__":
    main()
