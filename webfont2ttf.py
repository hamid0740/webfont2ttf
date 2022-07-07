
# WOFF2 to TTF Conversion
from fontTools.ttLib import woff2
# WOFF to TTF Conversion
import struct
import zlib

# WOFF to TTF Conversion
def convert_woff_ttf(infilename, outfilename):
  infile = open(infilename, mode="rb")
  outfile = open(outfilename, mode="wb")
  WOFFHeader = {
    "signature": struct.unpack(">I", infile.read(4))[0],
    "flavor": struct.unpack(">I", infile.read(4))[0],
    "length": struct.unpack(">I", infile.read(4))[0],
    "numTables": struct.unpack(">H", infile.read(2))[0],
    "reserved": struct.unpack(">H", infile.read(2))[0],
    "totalSfntSize": struct.unpack(">I", infile.read(4))[0],
    "majorVersion": struct.unpack(">H", infile.read(2))[0],
    "minorVersion": struct.unpack(">H", infile.read(2))[0],
    "metaOffset": struct.unpack(">I", infile.read(4))[0],
    "metaLength": struct.unpack(">I", infile.read(4))[0],
    "metaOrigLength": struct.unpack(">I", infile.read(4))[0],
    "privOffset": struct.unpack(">I", infile.read(4))[0],
    "privLength": struct.unpack(">I", infile.read(4))[0]
  }
  outfile.write(struct.pack(">I", WOFFHeader["flavor"]))
  outfile.write(struct.pack(">H", WOFFHeader["numTables"]))
  maximum = list(filter(lambda x: x[1] <= WOFFHeader["numTables"], [(n, 2 ** n) for n in range(64)]))[-1]
  searchRange = maximum[1] * 16
  outfile.write(struct.pack(">H", searchRange))
  entrySelector = maximum[0]
  outfile.write(struct.pack(">H", entrySelector))
  rangeShift = WOFFHeader["numTables"] * 16 - searchRange
  outfile.write(struct.pack(">H", rangeShift))
  offset = outfile.tell()
  TableDirectoryEntries = []
  for i in range(0, WOFFHeader["numTables"]):
    TableDirectoryEntries.append({
      "tag": struct.unpack(">I", infile.read(4))[0],
      "offset": struct.unpack(">I", infile.read(4))[0],
      "compLength": struct.unpack(">I", infile.read(4))[0],
      "origLength": struct.unpack(">I", infile.read(4))[0],
      "origChecksum": struct.unpack(">I", infile.read(4))[0]
    })
    offset += 4 * 4
  for TableDirectoryEntry in TableDirectoryEntries:
    outfile.write(struct.pack(">I", TableDirectoryEntry["tag"]))
    outfile.write(struct.pack(">I", TableDirectoryEntry["origChecksum"]))
    outfile.write(struct.pack(">I", offset))
    outfile.write(struct.pack(">I", TableDirectoryEntry["origLength"]))
    TableDirectoryEntry["outOffset"] = offset
    offset += TableDirectoryEntry["origLength"]
    if (offset % 4) != 0:
      offset += 4 - (offset % 4)
  for TableDirectoryEntry in TableDirectoryEntries:
    infile.seek(TableDirectoryEntry["offset"])
    compressedData = infile.read(TableDirectoryEntry["compLength"])
    if TableDirectoryEntry["compLength"] != TableDirectoryEntry["origLength"]:
      uncompressedData = zlib.decompress(compressedData)
    else:
      uncompressedData = compressedData
    outfile.seek(TableDirectoryEntry["outOffset"])
    outfile.write(uncompressedData)
    offset = TableDirectoryEntry["outOffset"] + TableDirectoryEntry["origLength"]
    padding = 0
    if (offset % 4) != 0:
      padding = 4 - (offset % 4)
    outfile.write(bytearray(padding))

# WOFF2 to TTF Conversion
def convert_woff2_ttf(infilename, outfilename):
  infile = open(infilename, "rb")
  outfile = open(outfilename, "wb")
  woff2.decompress(infile, outfile)

filename = input("Enter woff or woff2 file name: ")
if filename.split(".")[-1].lower() == "woff":
  try:
    convert_woff_ttf(filename, f"{'.'.join(filename.split('.')[:-1])}.ttf")
    print("[✓] Converted woff to ttf successfully.")
  except:
    print("[X] Couldn't convert woff to ttf.")
elif filename.split(".")[-1].lower() == "woff2":
  try:
    convert_woff2_ttf(filename, f"{'.'.join(filename.split('.')[:-1])}.ttf")
    print("[✓] Converted woff2 to ttf successfully.")
  except:
    print("[X] Couldn't convert woff2 to ttf.")
else:
  print("[X] File format is not good. Only woff & woff2")