# This program uses the shapely library

## Read SVG file
# Import libraries
import xml.etree.ElementTree as ET
from pathlib import Path

# Define path to SVG file
inputFile = "drawing.svg"
inputRoot = Path("svg-input") / inputFile

# Check if file exists
if not inputRoot.exists():  # Exit the program if the file is missing
    print(f"Error: SVG file at {inputRoot} was not found!")
    exit(1)
else:   # Otherwise start the import
    print(f"Importing SVG file: {inputFile}")

# Load SVG file
tree = ET.parse(inputRoot)
root = tree.getroot()
print(root)