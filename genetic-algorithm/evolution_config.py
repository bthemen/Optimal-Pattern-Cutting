import yaml
from dataclasses import dataclass

@dataclass
class EvolutionConfig:
    elite_size: int
    crossover_rate: float
    crossover_ratio: float
    mutation_rate: float

# Load from YAML
with open("evolution_config.yaml", "r") as f:
    data = yaml.safe_load(f)

config = EvolutionConfig(**data)