from src.models import Strategy

class FixedBettingStrategy(Strategy):
    def __init__(self,bet_amount: float, name: str = "Fixed Bet Strategy"):
        super().__init__(name)
        self.bet_amount = bet_amount

    def decide_bet(self, game_history):
        return self.bet_amount
    
class DoubleOnLossStrategy(Strategy):
    def __init__(self, base_bet: float, name: str = "Double On Loss Strategy"):
        super().__init__(name)
        self.base_bet = base_bet
        self.current_bet = base_bet

    def decide_bet(self, game_history):
        last = game_history.last_record()
        print("Last game record:", last)
        if not game_history.is_empty() and last["outcome"] == -1:
            self.current_bet *= 2
        else:
            self.current_bet = self.base_bet
        return self.current_bet