# Modules
import streamlit as st
import os
from fontTools.ttLib import woff2
import struct
import zlib
from helper import convert_woff_ttf, convert_woff2_ttf

# Main Function
def main():
  st.write("""# Webfont to TTF Converter
  ### Original Script: [Github](https://github.com/hamid0740/webfont2ttf)""")
  uploaded_file = st.file_uploader("Upload a webfont (WOFF, WOFF2):")
  if uploaded_file is not None:
    name = ".".join(uploaded_file.name.split(".")[:-1])
    format = uploaded_file.name.split(".")[-1].lower()
    if format in ["woff", "woff2"]:
      bytes_data = uploaded_file.getvalue()
      os.makedirs("./temp", exist_ok=True)
      fn = 1
      while True:
        if not os.path.isfile(f"./temp/{fn}/{fn}.{format}"):
          filename = f"./temp/{fn}/{fn}.{format}"
          os.makedirs(f"./temp/{fn}", exist_ok=True)
          with open(filename, "wb") as file:
            file.write(uploaded_file.getvalue())
          break
        else:
          fn += 1 
      if format == "woff":
        try:
          convert_woff_ttf(filename, f"./temp/{fn}/{fn}.ttf")
          st.write("✅️ Converted WOFF to TTF successfully.")
          st.download_button(label="Download converted TTF", data=open(f"./temp/{fn}/{fn}.ttf", "r").read(), file_name=f"{name}.ttf", mime="font/ttf")
        except:
          st.write("❌️ Couldn't convert WOFF to TTF.")
      elif format == "woff2":
        try:
          convert_woff2_ttf(filename, f"./temp/{fn}/{fn}.ttf")
          st.write("✅️ Converted WOFF2 to TTF successfully.")
          st.download_button(label="Download converted TTF", data=open(f"./temp/{fn}/{fn}.ttf", "r").read(), file_name=f"{name}.ttf", mime="font/ttf")
        except:
          st.write("❌️ Couldn't convert WOFF2 to TTF.")
      os.remove(f"./temp/{fn}")
    else:
      st.write("⚠️ Please upload a webfont only!")

if __name__ == "__main__":
  main()