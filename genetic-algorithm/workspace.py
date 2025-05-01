class Workspace:
    # Constructor
    def __init__(self, width: int, length: int, step: int, tolerance: int) -> None:
        self.width      = width     # Workspace width [mm]
        self.length     = length    # Workspace length [mm]
        self.step       = step      # Step size of workspace grid [mm]
        self.tolerance  = tolerance # Tolerance workspace overlap [mm]

    # String representation
    def __str__(self) -> str:
        return f"Workspace {self.width}x{self.length}"
    
    # Development representation
    def __repr__(self) -> str:
        return f"Workspace(width={self.width}, length={self.length}, step={self.step}, tolerance={self.tolerance})"