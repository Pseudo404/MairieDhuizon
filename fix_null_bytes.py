with open('core/views_app_mobile.py', 'rb') as f:
    raw = f.read()

# The file is a mix of UTF-8 and UTF-16LE.
# I will find the boundary.
utf16_start = raw.find(b'\xff\xfe')
if utf16_start == -1:
    # Maybe no BOM? Let's just remove all null bytes from the whole file if it's mostly ascii/utf-8.
    # Actually wait, removing null bytes works for ascii characters in UTF-16LE.
    cleaned = raw.replace(b'\x00', b'').decode('utf-8', errors='ignore')
else:
    part1 = raw[:utf16_start].decode('utf-8')
    part2 = raw[utf16_start+2:].decode('utf-16le')
    cleaned = part1 + part2

# Let's just do a clean replace:
cleaned = raw.replace(b'\x00', b'').decode('utf-8', errors='ignore')

with open('core/views_app_mobile.py', 'w', encoding='utf-8') as f:
    f.write(cleaned)
