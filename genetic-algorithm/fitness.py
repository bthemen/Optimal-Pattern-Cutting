import numpy as np

class Fitness:
    def __init__(self, genome: np.array) -> float:
        # Index spacing
        spacing = 2

        # TODO: take ultima from bounds method
        # x direction
        x_min = min(genome[0, 1::spacing]) # Minimum x value
        x_max = max(genome[0, 1::spacing]) # Maximum x value

        # y direction
        y_min = min(genome[0, 2::spacing]) # Minimum y value
        y_max = max(genome[0, 2::spacing]) # Maximum y value

        # Calculate effective area
        effective_area = (x_max - x_min) * (y_max - y_min)

        return effective_area