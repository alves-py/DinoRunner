from dino_runner.utils.constants import HEART, DEFAULT_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Small_heart(PowerUp):
    def __init__(self):
        self.image = HEART
        self.type = DEFAULT_TYPE
        super().__init__(self.image, self.type)