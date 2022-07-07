# Modules
from fontTools.ttLib import TTFont, woff2

# WOFF to TTF Conversion
def convert_woff_ttf(infilename, outfilename):
  infile = TTFont(infilename)
  infile.falvor = None
  infile.save(outfilename)

# WOFF2 to TTF Conversion
def convert_woff2_ttf(infilename, outfilename):
  infile = open(infilename, "rb")
  outfile = open(outfilename, "wb")
  woff2.decompress(infile, outfile)

# Main function
def main():
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
  
if __name__ == "__main__":
  main()
