import numpy as np
from workspace import Workspace

class Genome:
    # Constructor
    def __init__(self, genome_length: int) -> None:
        # TODO: Change exception to divisible by 3 after adding rotation
        # Exceptions
        if genome_length <= 0 or genome_length % 2 != 0:
            raise ValueError("Genome length must be a positive even number.")
        
        # Define fields
        self.length = genome_length # Number of variables in design vector
        self.design_vector: np.ndarray | None = None    # Initialize design vector

    # Create random genome
    def random_genome(self, ws: Workspace) -> None:
        # Exceptions
        if not isinstance(ws, Workspace):
            raise TypeError("Expected a Workspace instance.")

        # Create random values for the x and y coordinates of the pattern piece centers
        sliced_len = self.length // 2
        random_value_x = ws.width * np.random.uniform(0, 1, size=sliced_len)
        random_value_y = ws.length * np.random.uniform(0, 1, size=sliced_len)
        # TODO: add rotation of pattern pieces

        # Fill genome
        design_vector = np.zeros([1, self.length])
        for i in range(sliced_len):
            design_vector[0, 2 * i]       = random_value_x[i]
            design_vector[0, 2 * i + 1]   = random_value_y[i]

        self.design_vector = design_vector

    # Calculate fitness
    def calculate_fitness(self) -> float:
        # Exceptions
        if self.design_vector is None:
            raise ValueError("Design vector has not been initialized.")

        # Index spacing
        spacing = 2

        # TODO: take ultima from bounds method
        # Separate x and y values from the design vector
        x_values = self.design_vector[0, 0::spacing]
        y_values = self.design_vector[0, 1::spacing]

        x_min, x_max = np.min(x_values), np.max(x_values)
        y_min, y_max = np.min(y_values), np.max(y_values)

        # Calculate effective area
        return (x_max - x_min) * (y_max - y_min)

    # String representation
    def __str__(self) -> str:
        if self.design_vector is None:
            return f"Genome with no set design vector"
        return f"Genome with design vector: {self.design_vector}"

    # Developer representation
    def __repr__(self) -> str:
        return f"Genome(length={self.length}, design_vector={self.design_vector})"