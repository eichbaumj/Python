#!/usr/bin/env python3

import sqlite3
import binascii
import sys
from Cryptodome.Cipher import AES
import struct

def rfc3394_key_unwrap(kek: bytes, wrapped: bytes) -> bytes:
    """
    Pure-Python AES Key Unwrap (RFC 3394) implementation.
    Unwraps the 'wrapped' key with the 128-bit or 256-bit 'kek'.
    Returns the unwrapped key bytes or raises ValueError on integrity check fail.
    """
    # Check length: must be multiple of 8 bytes and >= 16
    n = len(wrapped) // 8
    if n < 2:
        raise ValueError("Input too short for key unwrap")
    if len(wrapped) % 8 != 0:
        raise ValueError("Wrapped key not aligned to 64-bit boundary")

    # The default IV per RFC 3394
    a = struct.unpack(">Q", wrapped[:8])[0]  # 64-bit integer
    r = [wrapped[8+8*i:16+8*i] for i in range(n-1)]

    # AES-ECB with the KEK
    aes_ecb = AES.new(kek, AES.MODE_ECB)

    # 6*(n-1) rounds
    for j in range(5, -1, -1):         # j=5..0
        for i in range(n-1, 0, -1):    # i=(n-1)..1
            t = (n-1)*j + i
            # B = AES-1(A ^ t, R[i])
            block = struct.pack(">Q", a ^ t) + r[i-1]
            b = aes_ecb.decrypt(block)
            a = struct.unpack(">Q", b[:8])[0]
            r[i-1] = b[8:]

    # Check integrity
    if a != 0xA6A6A6A6A6A6A6A6:
        raise ValueError("Integrity check failed in key unwrap")

    return b"".join(r)

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <NoteStore.sqlite> <kek_hex> [<pk>]")
        sys.exit(1)

    db_path = sys.argv[1]
    kek_hex = sys.argv[2]
    pk_filter = int(sys.argv[3]) if len(sys.argv) > 3 else None

    # Convert KEK from hex to bytes
    kek = binascii.unhexlify(kek_hex)

    # Connect to DB and query
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if pk_filter:
        query = """
        SELECT Z_PK, ZCRYPTOWRAPPEDKEY
        FROM ZICCLOUDSYNCINGOBJECT
        WHERE ZISPASSWORDPROTECTED=1 AND Z_PK=?
        """
        rows = cursor.execute(query, (pk_filter,)).fetchall()
    else:
        query = """
        SELECT Z_PK, ZCRYPTOWRAPPEDKEY
        FROM ZICCLOUDSYNCINGOBJECT
        WHERE ZISPASSWORDPROTECTED=1
        """
        rows = cursor.execute(query).fetchall()

    conn.close()

    if not rows:
        print("[!] No locked notes found.")
        return

    for (pk, wrapped_key_blob) in rows:
        if not wrapped_key_blob:
            print(f"[!] Note PK={pk}: no wrapped key data.")
            continue

        # Attempt RFC3394 unwrap
        try:
            unwrapped_key = rfc3394_key_unwrap(kek, wrapped_key_blob)
            unwrapped_hex = binascii.hexlify(unwrapped_key).decode()
            print(f"Note PK={pk}: Unwrapped Key (hex) = {unwrapped_hex}")
        except ValueError as e:
            print(f"[Error] Could not unwrap key for note {pk}: {e}")

if __name__ == "__main__":
    main()
