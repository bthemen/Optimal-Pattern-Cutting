## Import libraries
# Root directory
import xml.etree.ElementTree as ET
from pathlib import Path

# SVG files
from svg.path import parse_path, Line, CubicBezier, Move, Close, Arc, QuadraticBezier

# Numeric calculations
import numpy as np
import math

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
svg_paths = root.findall(".//svg:path", ns)

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
#   C 80.4,53.2 68.3,48.7 54.8,50.8 --> Cubic Bezier curve from (92.2, 58.7) to (54.8, 50.8) with control points (80.4, 53.2) and (68.3, 48.7)
#   Z --> Close the curve
# Since Bezier curves are smooth, a polygon has to be approximated through discretization.

# Fetch path objects
paths = []
for svg_path in svg_paths:
    d_attr = svg_path.get("d")  # Get the SVG d attribute
    if d_attr:
        path = parse_path(d_attr)   # Convert to path object
        paths.append(path)          # Store path objects

print(f"Found {len(paths)} pattern pieces")

## Extract polygon coordinates from path objects
# Define cubic Bezier function
def cubic_bezier(t, p0, p1, p2, p3):
    """
    Calculate a point on a cubic Bezier curve.
    :param t: The parameter t (0 <= t <= 1)
    :param p0, p1, p2, p3: Control points
    :return: The point on the curve at t
    """
    return ((1 - t) ** 3 * p0 + 
            3 * (1 - t) ** 2 * t * p1 +
            3 * (1 - t) * t ** 2 * p2 + 
            t ** 3 * p3)

# Extract coordinates
coordinates = []

step_size = 1  # Step size of workspace grid [mm]

for path in paths:  # Loop over all pattern pieces
    coords = []
    for segment in path:    # Loop over all path segments
        if isinstance(segment, Move):           # Move to
                coords.append((segment.end.real, segment.end.imag))
        elif isinstance(segment, Line):         # Line to
                coords.append((segment.end.real, segment.end.imag))
        elif isinstance(segment, CubicBezier):  # Cubic Bezier curve
                # Extract data from segment
                p0 = np.array([segment.start.real, segment.start.imag])
                p1 = np.array([segment.control1.real, segment.control1.imag])
                p2 = np.array([segment.control2.real, segment.control2.imag])
                p3 = np.array([segment.end.real, segment.end.imag])

                # Generate points along the curve
                curve_length = segment.length(error=1e-5)
                num_points = math.ceil(curve_length / step_size)

                for i in range(num_points - 1):
                    t = (i + 1) / (num_points - 1)  # t goes from 0 to 1
                    point = cubic_bezier(t, p0, p1, p2, p3)

                    coords.append(point.tolist())

        elif isinstance(segment, Close):        # Close path
                pass
        else:
                print(f"Unhandled segment type: {type(segment)}")

    coordinates.append(coords)

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