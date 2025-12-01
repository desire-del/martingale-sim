from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd


class Strategy(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def decide_bet(self, game_history) -> float:
        """Decide the next bet size based on the provided `History`.

        Must return a numeric bet (float)."""
        raise NotImplementedError

    def description(self) -> str:
        return f"Strategy Name: {self.name}"
    
class Game(ABC):
    def __init__(self, title: str):
        self.title = title
        self.description = ""

    @abstractmethod
    def play_round(self, game_history) -> float:
        """Simulate one round and return the outcome multiplier for the bet.

        For example, return -1.0 for losing the bet, or +1.0 for winning an equal amount.
        """
        raise NotImplementedError

    def info(self) -> str:
        return f"Game Title: {self.title}"
    
class History:
    """Class to keep track of game history."""
    def __init__(self):
        self.records = pd.DataFrame(columns=["outcome", "bet", "total_gain"])

    def add_record(self, outcome: float, bet: float, total_gain: float) -> None:
        new_record = pd.DataFrame([{"outcome": outcome, "bet": bet, "total_gain": total_gain}])
        self.records = pd.concat([self.records, new_record], ignore_index=True)

    def last_record(self) -> pd.Series:
        if not self.records.empty:
            return self.records.iloc[-1]
        else:
            return pd.Series()
    def is_empty(self) -> bool:
        return self.records.empty
        
    def get_capital(self) -> pd.Series:
        return self.records["total_gain"].values
    
    def get_bets(self) -> pd.Series:
        return self.records["bet"].values
    
    def get_outcomes(self) -> pd.Series:
        return self.records["outcome"].values
    
    def expected_value(self) -> float:
        if not self.records.empty:
            return self.records["outcome"].mean()
        else:
            return 0.0
    def max_drawdown(self) -> float:
        if not self.records.empty:
            cumulative_max = self.records["total_gain"].cummax()
            drawdowns = cumulative_max - self.records["total_gain"]
            return drawdowns.max()
        else:
            return 0.0
    def length(self) -> int:
        return len(self.records)
    
    def variance_gain(self) -> float:
        if not self.records.empty:
            return self.records["total_gain"].var()
        else:
            return 0.0
    def get_records(self) -> pd.DataFrame:
        return self.records
    
class Result:
    def __init__(self, history: pd.DataFrame):
        self.history = history
        self.total_rounds = len(history)
        self.final_gain = history["total_gain"].iloc[-1] if self.total_rounds > 0 else 0.0    
    def compute_statistics(self) -> dict:
        stats = {
            "total_rounds": self.total_rounds,
            "final_gain": self.final_gain,
            "average_bet": self.history["bet"].mean() if self.total_rounds > 0 else 0.0,
            "max_bet": self.history["bet"].max() if self.total_rounds > 0 else 0.0,
            "min_bet": self.history["bet"].min() if self.total_rounds > 0 else 0.0,
            "max_drawdown": (self.history["total_gain"].cummax() - self.history["total_gain"]).max() if self.total_rounds > 0 else 0.0
        }
        return stats
    
class Simulation:

    def __init__(self, strategies: list[Strategy], game: Game, max_bet: float = 1000.0, start_value: float = 100.0):
        self.strategies = strategies
        self.game = game
        self.max_bet = max_bet
        self.start_value = start_value
        # `self.history` remains available as a convenience, but each strategy
        # will be simulated with an independent `History` instance inside `run`.
        self.history = History()

    def run(self, rounds: int, stop_condition=None) -> None:
        results = {}

        for strategy in self.strategies:
            # Independent history and capital for each strategy
            history = History()
            gain = float(self.start_value)

            for _ in range(rounds):
                bet = strategy.decide_bet(history)

                # Basic validation and clipping
                if bet is None:
                    bet = 0.0
                try:
                    bet = float(bet)
                except Exception:
                    raise TypeError(f"Strategy `{strategy.name}` returned non-numeric bet: {bet}")

                if bet < 0:
                    raise ValueError(f"Strategy `{strategy.name}` returned negative bet: {bet}")

                if bet > self.max_bet:
                    bet = float(self.max_bet)

                outcome = self.game.play_round(history)
                gain += bet * outcome

                history.add_record(outcome=float(outcome), bet=float(bet), total_gain=float(gain))

                if stop_condition and stop_condition(history):
                    break

            results[strategy.name] = Result(history.get_records())

        return results

    def get_history(self) -> pd.DataFrame:
        return self.history.get_records()