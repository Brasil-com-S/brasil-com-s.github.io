import os
import csv
import json
import urllib.request
import subprocess

# Create logo subdirectories
os.makedirs("assets/logos/original", exist_ok=True)
os.makedirs("assets/logos/gemini", exist_ok=True)

# Copy existing SVG and PNG logos to assets/logos/gemini/
for f in os.listdir("assets/logos"):
    if f.endswith(".png") or f.endswith(".svg") or f.endswith(".jpg"):
        src = os.path.join("assets/logos", f)
        if os.path.isfile(src):
            dst = os.path.join("assets/logos/gemini", f)
            shutil.copyfile(src, dst)

print("Organized Gemini logos into assets/logos/gemini/")
