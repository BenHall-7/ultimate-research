import struct
import zstd

def decompress(f):
    dc = zstd.ZstdDecompressor()
    return dc.decompress(f, max_output_size=100000000)

def isascii(b):
    for i in b:
        if not(i in range(0x30, 0x40) or i in range(65, 91) or i in range(97, 122)):
            return False
    return True

with open('Find.csv', 'r') as csv:
    offsets = [int(i.split(',')[0].rstrip('h'), base=16) for i in csv.readlines()]

offset_count = len(offsets)

magics = []

with open('data.arc', 'rb') as arc:
    for i, offset in enumerate(offsets):
        if i % 1000 == 0:
            print('{}%'.format((100 * i) / offset_count))
        arc.seek(offset)
        if i + 1 != len(offsets):
            compressed_bytes = arc.read(offsets[i+1] - offset).rstrip(b'\x00')
            try:
                decompressed_bytes = decompress(compressed_bytes)
            except:
                with open('compressed_files/{}.bin'.format(hex(offset)), 'wb') as f:
                    f.write(compressed_bytes)
            else:
                with open('decompressed_files/{}.bin'.format(hex(offset)), 'wb') as f:
                    f.write(decompressed_bytes)
