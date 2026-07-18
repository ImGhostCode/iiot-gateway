import math
import time


class SineGenerator:
    def generate(self):
        return round(
            50 + 20 * math.sin(time.time() / 5),
            2,
        )