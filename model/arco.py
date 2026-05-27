from dataclasses import dataclass
from model.pilota import Pilota

@dataclass
class Arco:
    d1: Pilota
    d2: Pilota
    peso: int