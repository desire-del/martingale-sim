from src.models import Game
import numpy as np

class BenoulliProcess(Game):
    def __init__(self, title: str = "Bernoulli Process", p: float = 0.5):
        super().__init__(title)
        self.p = p

    def play_round(self, game_history):
        return 1 if np.random.rand() < self.p else -1
    

class RandomWalkGame(Game):
    def __init__(self, a, b, p=0.5, title="Random Walk Game"):
        super().__init__(title)
        self.a = a
        self.b = b
        self.p = p
        self.position = 0
        self.step_list = []

    def play_round(self, game_history):
        r = np.random.rand()
        
        step = 1 if r < self.p else -1
        self.step_list.append(step)
        self.position += step

        # Win if inside [a, b]
        if self.a <= self.position <= self.b:
            return 1
        else:
            return -1