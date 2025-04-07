## Import libraries
# Root directory
import xml.etree.ElementTree as ET
from pathlib import Path

# SVG files
from svg.path import parse_path, Line, CubicBezier, Move, Close, Arc, QuadraticBezier

# Numeric calculations
import numpy as np

# Polygon creation
from shapely.geometry import Polygon

## Read SVG file
# Define path to SVG file
inputFile = "overlap_advanced.svg"
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
# For example the simple paths in disjoint.svg: <path d="M 60.7,41.1 45.0,62.5 68.9,71.1 Z" />
# This means:
#   M 60.7,41.1 --> Move to (60.7, 41.1) / create initial vertex at (60.7, 41.1)
#   L 45.0,62.5 --> Line to (45.0, 62.5) / create a line from (60.7, 41.1) to (45.0, 62.5)
#   L 68.9,71.1 --> Line to (68.9, 71.1) / create a line from (45.0, 62.5) to (68.9, 71.1)
#   Z --> Close the polygon / create a line from (68.9, 71.1) to (60.7, 41.1)

# A more complex example is the Bezier curve in overlap_advanced.svg:
# <path d="M 54.8,50.8 66.2,67.5 92.2,58.7 C 80.4,53.2 68.3,48.7 54.8,50.8 Z" />
#   M 54.8,50.8 --> Move to (54.8, 50.8) / create initial vertex at (54.8, 50.8)
#   L 66.2,67.5 --> Line to (66.2, 67.5) / create a line from (54.8, 50.8) to (66.2, 67.5)
#   L 92.2,58.7 --> Line to (92.2, 58.7) / create a line from (66.2, 67.5) to (92.2, 58.7)
#   C 80.4,53.2 68.3,48.7 54.8,50.8 --> Cubic Bezier curve to (54.8, 50.8) with control points (80.4, 53.2) and (68.3, 48.7)
#   Z --> Close the curve
# Since Bezier curves are smooth, a polygon has to be approximated through discretization.

# Parse SVG d attribute
def parse_svg_path(d_attr):
    """
    Convert an SVG path string to a list of coordinates.
    This function assumes simple paths with 'M' (move to) and 'L' (line to).
    More complex paths (e.g. Bezier curves) will require additional parsing.
    """
    points = []                 # Initialize list of points
    
    if "C" not in d_attr:   # Simple paths
        commands = d_attr.split()   # Split string by space
        for cmd in commands:
            if cmd[0].isalpha():    # Ignore command letters
                continue

            x, y = map(float, cmd.strip(",").split(","))    # Convert string to float pairs in a map
            points.append((x, y))   # Add map to the list of points

    else:   # Paths containing Bezier curves
        path = parse_path(d_attr)   # Parse the d attribute

        for segment in path:

            print(segment.length())

            if isinstance(segment, Move):   # Move to
                points.append((segment.end.real, segment.end.imag))
            elif isinstance(segment, Line): # Line to
                points.append((segment.end.real, segment.end.imag))
            elif isinstance(segment, CubicBezier):  # Cubic Bezier curve
                points.append((segment.control1.real, segment.control1.imag, segment.control2.real, segment.control2.imag, segment.end.real, segment.end.imag))
            elif isinstance(segment, QuadraticBezier):  # Quadratic Bezier curve
                points.append((segment.control.real, segment.control.imag, segment.end.real, segment.end.imag))
            elif isinstance(segment, Arc):  # Arc
                points.append((segment.end.real, segment.end.imag))
            elif isinstance(segment, Close):    # Close path
                pass
            else:
                print(f"Unhandled segment type: {type(segment)}")

    return points

# Fetch coordinates
coordinates = []
for path in paths:
    d_attr = path.get("d")  # Get the SVG d attribute
    if d_attr:
        coord = parse_svg_path(d_attr)  # Convert to coordinates
        coordinates.append(coord)       # Store coordinates

print(f"Found {len(coordinates)} pattern pieces")



paths, attributes = svg2paths(inputRoot)
print(paths)
print(attributes)
exit(1)

## Discretizing Bezier curve
# Define cubic Bezier function
def cubic_bezier(t, p0, p1, p2, p3):
    """
    Calculate a point on a cubic Bezier curve.
    :param t: The parameter t (0 <= t <= 1)
    :param p0, p1, p2, p3: Control points
    :return: The point on the curve at t
    """
    return ((1 - t) ** 3 * np.array(p0) + 
            3 * (1 - t) ** 2 * np.array(p1) +
            3 * (1 - t) * t ** 2 * np.array(p2) + 
            t ** 3 * np.array(p3))

# Extract the control points from the Bezier path

## Overlap detection


# Create polygons
polygons = []
for coords in coordinates:
    polygons.append(Polygon(coords))    # Create a Shapely polygon

def check_for_overlaps(polygons):
    """
    Check if any of the presented polygons overlap.
    """

    overlap = False # Initialize

    for i in range(len(polygons)):
        for j in range(i + 1, len(polygons)):
            if polygons[i].intersects(polygons[j]): # Check if jth Polygon overlaps with ith Polygon
                print(f"Piece {i} overlaps with Piece {j}")
                overlap = True

    if not overlap: # Check if Polygons do not overlap
        print("Pieces do not overlap")

    return overlap

check_for_overlaps(polygons)