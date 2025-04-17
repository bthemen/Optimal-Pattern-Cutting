## Import libraries
# Root directory
from pathlib import Path
from lxml import etree

# SVG files
from svg.path import parse_path, Line, CubicBezier, Move, Close, Arc, QuadraticBezier

# Numeric calculations
import numpy as np
import math

# Polygon creation
from shapely.geometry import Polygon
from shapely.affinity import translate, rotate

## Workspace parameters
ws_width = 1300     # Workspace width [mm]
ws_height = 2500    # Workspace height [mm]
ws_step = 10        # Step size of workspace grid [mm]
ws_tolerance = 10   # Tolerance workspace overlap [mm]

## Units
def px_to_mm(pixels, dpi=96):
    return pixels * 25.4 / dpi

def mm_to_px(mm, dpi=96):
    return mm * dpi / 25.4

## Read SVG file
# Define path to SVG file
inputFile = "rin-final-v2.svg"
inputRoot = Path("svg-input") / inputFile

# Check if file exists
if not inputRoot.exists():  # Exit the program if the file is missing
    print(f"Error: SVG file at {inputRoot} was not found!")
    exit(1)
else:   # Otherwise start the import
    print(f"Importing SVG file: {inputFile}")

# Load SVG file
tree = etree.parse(inputRoot)
root = tree.getroot()

## Decipher SVG file
# Check for invalid paths
def check_invalid_paths(element):
    while element is not None:  # Loop until first element is found
        if element.tag.endswith("clipPath") or element.tag.endswith("defs"):
            return True
        element = element.getparent()   # Go to parent element
    return False

# Extract path 
def extract_paths(svg_root):
    # Initialize list
    paths = []

    for element in svg_root.iter():
        # Only process <path> elements NOT inside <clipPath> or <defs>
        if element.tag.endswith("path") and not check_invalid_paths(element):
            d = element.get("d")
            if d:
                paths.append(element)
    return paths

# List all suitable path elements
svg_paths = extract_paths(root)

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

pattern_number = len(paths)     # Number of pattern pieces
print(f"Found {pattern_number} pattern pieces")

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

for piece, path in enumerate(paths):  # Loop over all pattern pieces
    coords = []
    for i, segment in enumerate(path):    # Loop over all path segments
        if isinstance(segment, Move):           # Move to
                coords.append(px_to_mm(np.array([segment.end.real, segment.end.imag])))
        elif isinstance(segment, Line):         # Line to
                coords.append(px_to_mm(np.array([segment.end.real, segment.end.imag])))
        elif isinstance(segment, CubicBezier):  # Cubic Bezier curve
                # Extract data from segment
                p0 = np.array((segment.start.real, segment.start.imag))
                p1 = np.array((segment.control1.real, segment.control1.imag))
                p2 = np.array((segment.control2.real, segment.control2.imag))
                p3 = np.array((segment.end.real, segment.end.imag))

                # Generate points along the curve
                curve_length = segment.length(error = 1e-5)
                num_points = math.ceil(curve_length / ws_step)

                for j in range(num_points - 1):
                    t = (j + 1) / (num_points - 1)  # t goes from 0 to 1
                    point = cubic_bezier(t, p0, p1, p2, p3)

                    coords.append(px_to_mm(point))

        elif isinstance(segment, Close):        # Close path
                pass
        else:
                print(f"Unhandled segment type: {type(segment)}")

    coordinates.append(coords)

## Create polygons
polygons = []
for coords in coordinates:
    polygons.append(Polygon(coords))    # Create a Shapely polygon

## Centroid calculation
# Calculate the geometric center of each polygon
centroids = np.empty((pattern_number, 2), dtype=float)
for i, polygon in enumerate(polygons):
     centroids[i] = np.array((polygon.centroid.x, polygon.centroid.y))

## Moving centroids
translation = [0, 0]
rotation = 15

new_polygons = []
for polygon in polygons:
     p = translate(polygon, xoff=translation[0], yoff=translation[1])
     new_polygons.append(rotate(p, angle=rotation))


## Overlap detection
# Between pattern pieces
def pattern_overlap(polygons):
    """
    Check if any of the presented polygons overlap.
    """

    # Initialize
    overlap_status = False
    overlap_pieces = []

    for i in range(len(polygons)):
        for j in range(i + 1, len(polygons)):
            if polygons[i].intersects(polygons[j]): # Check if jth Polygon overlaps with ith Polygon
                print(f"Piece {i} overlaps with Piece {j}")
                overlap_status = True
                overlap_pieces.append((i, j))

    if not overlap_status: # Check if Polygons do not overlap
        print("Pattern pieces do not overlap with each other")

    return overlap_pieces

# With workspace
def workspace_overlap(polygons, width=ws_width, height=ws_height):
    """
    Check if any of the pattern piece fall outside of the workspace
    """

    # Initialize
    overlap_status = False
    overlap_ws = []

    for i, polygon in enumerate(polygons):
        # Extract coordinates
        coords = polygon.exterior.coords

        # Find maximum and minimum
        coord_max = np.max(coords, axis=0)
        coord_min = np.min(coords, axis=0)

        # Check if coordinates overlap with workspace
        if coord_max[0] > width - ws_tolerance:
            overlap_status = True
            print(f"Pattern piece {i} exceeds maximum workspace width")
        if coord_max[1] > height - ws_tolerance:
            overlap_status = True
            print(f"Pattern piece {i} exceeds maximum workspace height")
        if coord_min[0] < ws_tolerance:
            overlap_status = True
            print(f"Pattern piece {i} exceeds minimum workspace width")
        if coord_min[1] < ws_tolerance:
            overlap_status = True
            print(f"Pattern piece {i} exceeds minimum workspace height")

        

    # Check if there is workspace overlap
    if not overlap_status:
        print("Pattern pieces do not overlap with workspace")

    return overlap_ws

overlap_pieces = pattern_overlap(new_polygons)
overlap_ws = workspace_overlap(new_polygons)

## Write new SVG file
def write_svg(polygons, ws_width, ws_height, output_filename="filtered_paths.svg"):
    output_dir = Path("svg-output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / output_filename.replace(".svg", "_discretized.svg")

    svg_ns = "http://www.w3.org/2000/svg"
    nsmap = {None: svg_ns}

    # Create SVG root element with width, height, and viewBox in mm
    svg = etree.Element("{%s}svg" % svg_ns, nsmap=nsmap)
    svg.set("version", "1.1")
    svg.set("width", f"{ws_width}mm")
    svg.set("height", f"{ws_height}mm")
    svg.set("viewBox", f"0 0 {ws_width} {ws_height}")

    # Create paths for each polygon
    for polygon in polygons:
        if not polygon:
            continue  # Skip empty polygons

        # Get the coordinates of the polygon and convert them into a list of points
        coordinates = polygon.exterior.coords

        # Build path data using M, L, and Z commands
        d_parts = [f"M {coordinates[0][0]} {coordinates[0][1]}"]
        d_parts += [f"L {x} {y}" for (x, y) in coordinates[1:]]
        d_parts.append("Z")  # Close the polygon

        d_attr = " ".join(d_parts)

        path = etree.Element("path")
        path.set("d", d_attr)
        path.set("fill", "none")  # Optional: outline only
        path.set("stroke", "red")
        path.set("stroke-width", "1")  # Optional: thin stroke for precision

        svg.append(path)

        # Create the <circle> element at the centroid with a radius of 20 mm (converted to pixels)
        centroid = (polygon.centroid.x, polygon.centroid.y)
        etree.SubElement(svg, '{http://www.w3.org/2000/svg}circle', cx=str(centroid[0]), cy=str(centroid[1]),
                                          r=str(5), fill="red")

    # Write the SVG to file
    tree = etree.ElementTree(svg)
    tree.write(str(output_path), pretty_print=True, xml_declaration=True, encoding="utf-8")

    print(f"SVG with discretized polygons written to {output_path}")

write_svg(new_polygons, ws_width, ws_height, inputFile)