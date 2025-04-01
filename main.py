# This program uses the shapely library

## Read SVG file
# Import libraries
import xml.etree.ElementTree as ET
from pathlib import Path

# Define path to SVG file
inputFile = "overlap.svg"
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

## Decipher SVG file
# Namespace for parsing SVG files correctly
ns = {'svg': 'http://www.w3.org/2000/svg'}

# Find all path elements
paths = root.findall(".//svg:path", ns)

# All polygons are stored in path elements. Their d attribute determines the shape.
# For example as in disjoint.svg: <path d="M 60.7,41.1 45.0,62.5 68.9,71.1 Z" />
# This means:
#   M 60.7,41.1 --> Move to (60.7, 41.1) / create initial vertex at (60.7, 41.1)
#   L 45.0,62.5 --> Line to (45.0, 62.5) / create a line from (60.7, 41.1) to (45.0, 62.5)
#   L 68.9,71.1 --> Line to (68.9, 71.1) / create a line from (45.0, 62.5) to (68.9, 71.1)
#   Z --> Close the polygon / create a line from (68.9, 71.1) to (60.7, 41.1)

# Parse SVG d attribute
def parse_svg_path(d_attr):
    """Convert an SVG path string to a list of coordinates."""
    points = []                 # Initialize list of points
    commands = d_attr.split()   # Split string by space
    for cmd in commands:
        if cmd[0].isalpha():    # Ignore command letters
            continue

        x, y = map(float, cmd.strip(",").split(","))    # Convert string to float pairs in a map
        points.append((x, y))   # Add map to the list of points
    return points

# Fetch coordinates
coordinates = []
for path in paths:
    d_attr = path.get("d")  # Get the SVG d attribute
    if d_attr:
        coord = parse_svg_path(d_attr)  # Convert to coordinates
        coordinates.append(coord)       # Store coordinates

print(coordinates)