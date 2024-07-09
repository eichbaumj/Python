#Python script designed to calculate CRC values for GPT Headers and Partition Entry Arrays
#James Eichbaum

import binascii

def calculate_crc32(data):
    return binascii.crc32(data) & 0xFFFFFFFF

header_data_hex = """
45 46 49 20 50 41 52 54 00 00 01 00 5C 00 00 00
00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00
AF D2 3B 77 00 00 00 00 22 00 00 00 00 00 00 00
8E D2 3B 77 00 00 00 00 55 BA 55 51 2B D8 59 41
BC 1F C4 17 80 0F D7 63 02 00 00 00 00 00 00 00
80 00 00 00 80 00 00 00 3B 5F D2 D0
"""

# Convert hex string to bytes
header_data = bytes.fromhex(header_data_hex.replace("\n", "").replace(" ", ""))

# Calculate CRC32
crc32_value = calculate_crc32(header_data)

# Convert CRC32 to hex string
crc32_hex = f"{crc32_value:08X}"

# Format the hex string in little-endian format for easy copying
little_endian_crc32 = ''.join([crc32_hex[i:i+2] for i in range(0, len(crc32_hex), 2)][::-1])
formatted_crc32 = ' '.join(little_endian_crc32[i:i+2] for i in range(0, len(little_endian_crc32), 2))

# Print CRC32 value and formatted hex
print(f"Calculated CRC32: {crc32_hex}")
print(f"Formatted for CRC field (little-endian): {formatted_crc32}")
